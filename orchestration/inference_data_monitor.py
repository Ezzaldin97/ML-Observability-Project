from flows.extract_prepare_flow import fetch_prepare_flow
from flows.inference_flow import inference_flow
from flows.data_monitoring_flow import data_monitoring_report_flow
from prefect import flow

@flow(name="InferenceAndDataDriftFlow", description="Batch Scoring and Data Drift Report",
      log_prints=True)
def parent_flow1(month:int, year:int) -> None:
    print("Inference Batch Scoring and Data Drift Detection Started...")
    file_path = f"./data/tmp/yellow_tripdata_{year}-{month:02}.parquet"
    fetch_prepare_flow(year, month)
    inference_flow(file_path)
    data_monitoring_report_flow(file_path, month, year)

if __name__ == "__main__":
    parent_flow1(3, 2021)