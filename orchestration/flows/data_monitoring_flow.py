from prefect import task, flow
import pandas as pd
import os
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
from evidently.metric_preset import DataQualityPreset

@task(name = "GetData", description = "Get Prepared Data",
      tags = ["Get", "Current", "Data"], log_prints = True)
def get_current_data(data_path:str) -> pd.DataFrame:
    print("Get Required Dataset")
    curr_df = pd.read_parquet(data_path)
    X_cols = ["PULocationID", "DOLocationID", "trip_distance"]
    return curr_df[X_cols]

@task(name = "DataMonitoringReport", description = "Generate and Save Data Monitoring Report",
      log_prints=True, tags = ["DataDrift", "DataQuality", "Report"])
def data_monitoring_report_generator(month:int, year:int, curr_df:pd.DataFrame) -> None:
    print("Generate Data Monitoring Report for Current Dataset")
    X_cols = ["PULocationID", "DOLocationID", "trip_distance"]
    ref_df = pd.read_parquet(os.path.join(".", "data", "ref", "yellow_tripdata_2021-01.parquet"))[X_cols]
    ref_sample = ref_df.sample(n = 100000, random_state=42)
    curr_sample = curr_df.sample(n = 100000, random_state = 42)
    report = Report(metrics=[
    DataDriftPreset(columns=X_cols,
                    stattest='kl_div',
                    num_stattest_threshold=0.2),
    DataQualityPreset(X_cols)
    ])
    report.run(reference_data=ref_sample, current_data=curr_sample)
    report.save_json(f"./reports/Data-Report-{month}-{year}.json")
    report.save_html(f"./reports/Data-Report-{month}-{year}.html")
    print("Data Saved Successfully as json and html formats")

@flow(name = "DataMonitoringFlow", description = "Generate Data Drift/Quality Report",
      log_prints=True)
def data_monitoring_report_flow(data_path:str, month:int, year:int) -> None:
    curr_df = get_current_data(data_path)
    data_monitoring_report_generator(month, year, curr_df)

