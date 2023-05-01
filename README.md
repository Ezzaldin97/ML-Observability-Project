# ML Observability Project:

## Description:

Create Monitoring System/Reports for ML Model in Production to Track the Model Performance in Production, Detect the Data Drift in Production and How it can affect the Model Performance, and check Data Integrity/Quality of the Data.

## Objective:

Getting Familiar with ML Observaility Concept, Use Evidently AI Package in Python which provides alot Metrics and Tests to Create Automatic Reports about Model Performance and Data, Simulate How to Create Batch Scoring Jobs/Data (Drift, Quality, Integrity) Jobs/Feedback of Batch Scoring Model Performance in Production.

The Objective here is to focus on ML Observability Concepts in Production Like Data Drift Detection, Measure Data Quality/Stability, and Measure the Performance of the Model, so the Development Process here is not important as much as Understanding Monitoring in Production works.

Optional We Can do Automatic retraining for the Model.

## Prerequisites:

- Git Bash in Windows or Linux OS
- Python >= 3.7 (I Used 3.7.9)
- Knowledge in ML

## Project Setup:

- install all python requirements needed to complete the project by running the following
```bash
pip install -r requirements.txt
```
- create a directory called data, and inside this directory create 3 other directories 
  - ref: for training dataset, this is our reference dataset.
  - validation: for validation dataset.
  - tmp: for datasets in production
- make sure to install wget command in your OS, and run the following
```bash
# inside data/ref
# use data of 2021-01 for training
wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet -O yellow_tripdata_2021-01.parquet
# inside data/validation
# use data of 2021-02 for validation
wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-02.parquet -O yellow_tripdata_2021-02.parquet
```
- run the flow of inference and data monitoring using the following:
```bash
python orchestration/inference_data_monitor.py --month {month} --year {year}
```
- run the flow of model performance using the following:
```bash
python orchestration/performance_feedback.py --month {month} --year {year}
```
- Reports Generated as json/html in reports directory.

## Use Case:

Using NYC Taxi Datasets, Predict the trip duration, and Use the Prediction of trip duration and Real Value of trip duration (can be calculated by taking the difference between drop off time and pick up time) to Calculate the Performance of the Model Using the Following:
```python
ref_sample = ref_df.sample(n = 100000, random_state=42)
curr_sample = curr_df.sample(n = 100000, random_state = 42)
report = Report(metrics = [
    RegressionPreset()
])
report.run(reference_data=ref_sample, current_data=curr_sample)
```
RegressionPreset here Provides alot of metrices to Measure the Performance of the Model on Data in production compared to its performance on training datasets.

also Using the Predictors of Training and Test Datasets, Generate Data Quality/Drift Report Using the Following
```python
ref_sample = ref_df.sample(n = 100000, random_state=42)
curr_sample = curr_df.sample(n = 100000, random_state = 42)
report = Report(metrics=[
    DataDriftPreset(columns=X_cols,
                    stattest='kl_div',
                    num_stattest_threshold=0.2),
    DataQualityPreset(X_cols)
])
report.run(reference_data=ref_sample, current_data=curr_sample)
```
here DataDriftPreset Used to Calculate Data Drift between Reference and Current Datasets, it provide alot of Statistical Measures that detect the divergence between both datasets, check the documentaion for more info.

## References:

- [DataTalks MLOps ZoomCamp Course](https://www.youtube.com/watch?v=3T5kUA3eWWc&list=PL3MmuxUbc_hIUISrluw_A7wDSmfOhErJK)
- [ML Observability Workshop](https://github.com/alexeygrigorev/ml-observability-workshop)
- [ML Observability Article](https://towardsdatascience.com/what-is-ml-observability-29e85e701688)
- [Evidently AI Data Drift Measures](https://www.evidentlyai.com/blog/data-drift-detection-large-datasets)
