import os
import pandas as pd
from prefect import task, flow
from prefect_shell import shell_run_command


@task(name = "PrepareData", description = "Prepare Data",
      tags = ["RawData", "Prepare"], retries = 2, log_prints=True)
def prepare(path:str) -> pd.DataFrame:
    df = pd.read_parquet(path)
    df["trip_duration"] = df["tpep_dropoff_datetime"] - df["tpep_pickup_datetime"]
    df["trip_duration"] = df["trip_duration"].dt.total_seconds() / 60.0
    df = df[(df["trip_duration"] >=1) & (df["trip_duration"] <= 60)]
    df = df[["PULocationID", "DOLocationID", "trip_distance", "trip_duration"]]
    print("Data Preparation Finished Successfully.")
    return df

@task(name = "SavePreparedData", description = "Save Prepared Data to start inference",
      tags = ["Save", "Data"], log_prints=True)
def save_prepared_data(df:pd.DataFrame, old_file_path:str) -> None:
    os.remove(old_file_path)
    df.to_parquet(old_file_path, compression = "gzip")
    print("Final Data Saved")

@flow(name = "FetchAndPrepareData", description = "Fetch Data From Source, Prepare it, and Save it",
      log_prints=True)
def fetch_prepare_flow(year:int, month:int) -> pd.DataFrame:
    source_path = f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year}-{month:02}.parquet"
    file_path = f"./data/tmp/yellow_tripdata_{year}-{month:02}.parquet"
    print("Read Data From Source")
    shell_run_command(command=f"wget {source_path} -O {file_path}", return_all=True)
    print("Data Fetched From Source Successfully")
    df = prepare(file_path)
    save_prepared_data(df, file_path)
