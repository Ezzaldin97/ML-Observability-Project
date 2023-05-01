from prefect import task, flow
import pandas as pd
import pickle
import os
from evidently.report import Report
from evidently.metric_preset import RegressionPreset

@task(name = "GetData", description = "Get Predictions and Target Variable",
      tags = ["Get", "Current", "Data"], log_prints = True)
def get_current_data(data_path:str) -> pd.DataFrame:
    print("Get Required Dataset")
    curr_df = pd.read_parquet(data_path)
    cols = ["prediction", "target"]
    return curr_df[cols]

@task(name = "PredictReferenceData", description = "Generate Predictions for Training Dataset",
      log_prints=True)
def prepare_predict_reference() -> pd.DataFrame:
    df = pd.read_parquet("./data/ref/yellow_tripdata_2021-01.parquet")
    df["trip_duration"] = df["tpep_dropoff_datetime"] - df["tpep_pickup_datetime"]
    df["trip_duration"] = df["trip_duration"].dt.total_seconds() / 60.0
    df = df[(df["trip_duration"] >=1) & (df["trip_duration"] <= 60)]
    with open("./bin/lgbm.pkl", "rb") as pkl_f:
        model = pickle.load(pkl_f)
    X_cols = ["PULocationID", "DOLocationID", "trip_distance"]
    predictions = model.predict(df[X_cols])
    df["prediction"] = predictions
    df.rename(columns = {"trip_duration":"target"}, inplace = True)
    cols = ["prediction", "target"]
    return df[cols]

@task(name = "PerformanceReport", description = "Generate and Save Model Performance Report",
      log_prints=True, tags = ["Model", "Performance", "Report"])
def performance_report_generator(month:int, year:int, curr_df:pd.DataFrame, ref_df:pd.DataFrame) -> None:
    print("Generate Model Performance Report for Current Dataset")
    ref_sample = ref_df.sample(n = 100000, random_state=42)
    curr_sample = curr_df.sample(n = 100000, random_state = 42)
    report = Report(metrics = [
        RegressionPreset()
    ])
    report.run(reference_data=ref_sample, current_data=curr_sample)
    report.save_json(f"./reports/Performance-Report-{month}-{year}.json")
    report.save_html(f"./reports/Performance-Report-{month}-{year}.html")
    print("Data Saved Successfully as json and html formats")

@flow(name = "PerformanceMonitoringFlow", description = "Generate Model Performance Report",
      log_prints=True)
def parent_flow2(month:int, year:int) -> None:
    print("Model Performance Report Generation Started...")
    file_path = f"./data/tmp/yellow_tripdata_{year}-{month:02}.parquet"
    curr_df = get_current_data(file_path)
    ref_df = prepare_predict_reference()
    performance_report_generator(month, year, curr_df, ref_df)
    os.remove(file_path)

if __name__ == "__main__":
    parent_flow2(3, 2021)