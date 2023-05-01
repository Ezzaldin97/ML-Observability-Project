import os
import pandas as pd
from prefect import task, flow
import pickle


@task(name = "LoadModel", description = "Load LGBM Model",
      tags = ["Load", "MLModel"], log_prints=True)
def load_model():
    print("Load Model from bin directory")
    with open(os.path.join(".", "bin", "lgbm.pkl"), "rb") as pkl_file:
        model = pickle.load(pkl_file)
    return model

@task(name = "Inference", description = "Generate Predicted Target Variable",
      tags = ["inference", "model", "predict", "target"], log_prints=True)
def generate_predictions(data_path:str, model) -> pd.DataFrame:
    print(f"Generate Predictions for {data_path}")
    df = pd.read_parquet(data_path)
    X_cols = ["PULocationID", "DOLocationID", "trip_distance"]
    predictions = model.predict(df[X_cols])
    # the following step will be used to simulate the process of creating model performance report
    # here will add the predictions to dataframe as prediction
    df["prediction"] = predictions
    # rename the true target column as "target"
    df.rename(columns = {"trip_duration":"target"}, inplace = True)
    # remove the old dataset and replace..
    os.remove(data_path)
    df.to_parquet(data_path, compression = "gzip", index = False)
    print("Inference Completed Successfully..")

@flow(name = "InferenceFlow", description = "Batch Scoring flow",
      log_prints=True)
def inference_flow(data_path:str) -> None:
    model = load_model()
    generate_predictions(data_path, model)