from azureml.core import Experiment
from azureml.pipeline.steps import ParallelRunConfig, ParallelRunStep
from azureml.pipeline.core import PipelineData
from azureml.pipeline.core import Pipeline
import requests

# Create a pipeline with a ParallelRunStep to handle batch input
###############################################################################
# Get the batch dataset for input
batch_data_set = ws.datasets["batch-data"]

# Set the output location as a PipelineData object
default_ds = ws.get_default_datastore()
output_dir = PipelineData(
    name="inferences",
    datastore=default_ds,
    output_path_on_compute="results"
)

# Define the parallel run step configuration
parallel_run_config = ParallelRunConfig(
    source_directory="batch_scripts",
    entry_script="batch_scoring_script.py",
    mini_batch_size="5",
    error_threshold=10,
    output_action="append_row",
    environment=batch_env,
    compute_target=aml_cluster,
    node_count=4
)

# Create the parallel run step
parallelrun_step = ParallelRunStep(
    name="batch-score",
    parallel_run_config=parallel_run_config,
    inputs=[batch_data_set.as_named_input("batch_data")],
    output=output_dir,
    arguments=[],
    allow_reuse=True
)
# Create the pipeline
pipeline = Pipeline(workspace=ws, steps=[parallelrun_step])
###############################################################################


# Consume the batch model (pipeline endpoint)
###############################################################################
# Run the pipeline as an experiment
pipeline_run = Experiment(ws, "batch_prediction_pipeline").submit(pipeline)
pipeline_run.wait_for_completion(show_output=True)

# Get the outputs from the first (and only) step
prediction_run = next(pipeline_run.get_children())
prediction_output = prediction_run.get_output_data("inferences")
prediction_output.download(local_path="results")

# Find the parallel_run_step.txt file
for root, dirs, files in os.walk("results"):
    for file in files:
        if file.endswith("parallel_run_step.txt"):
            result_file = os.path.join(root, file)

# Load and display the results
df = pd.read_csv(result_file, delimiter=":", header=None)
df.columns = ["File", "Prediction"]
print(df)
###############################################################################


# Publish batch pipeline
###############################################################################
published_pipeline = pipeline_run.publish_pipeline(
    name='Batch_Prediction_Pipeline',
    description='Batch pipeline',
    version='1.0'
)
rest_endpoint = published_pipeline.endpoint
###############################################################################


# Consume pipeline endpoint
###############################################################################
response = requests.post(
    rest_endpoint,
    headers=auth_header,
    json={"ExperimentName": "Batch_Prediction"}
)
run_id = response.json()["Id"]
###############################################################################
