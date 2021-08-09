from azureml.core import Workspace
from azureml.pipeline.core import Pipeline
from azureml.core import Experiment
from azureml.pipeline.steps import PythonScriptStep
import requests

ws = Workspace.from_config()

# Step to run a Python script
step1 = PythonScriptStep(
    name = "prepare data",
    source_directory = "scripts",
    script_name = "data_prep.py",
    compute_target = "aml-cluster"
)

# Step to train a model
step2 = PythonScriptStep(
    name = "train model",
    source_directory = "scripts",
    script_name = "train_model.py",
    compute_target = "aml-cluster"
)

# Construct the pipeline
train_pipeline = Pipeline(workspace = ws, steps = [step1, step2])

# Create an experiment and run the pipeline with it
experiment = Experiment(workspace = ws, name = "training-pipeline")
pipeline_run = experiment.submit(train_pipeline)
# To run all pipeline steps without cached results
# pipeline_run = experiment.submit(train_pipeline, regenerate_outputs=True)

# Publish the pipeline run
published_pipeline = pipeline_run.publish(
    name="training_pipeline",
    description="Model training pipeline",
    version="1.0"
)

# Get the endpoint for the published pipeline
rest_endpoint = published_pipeline.endpoint
print(rest_endpoint)
# Consume the pipeline through REST request
response = requests.post(
    rest_endpoint,
    headers=some_auth_header,
    json={"ExperimentName": "run_training_pipeline"})
run_id = response.json()["Id"]
print(run_id)