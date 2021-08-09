from azureml.pipeline.core.graph import PipelineParameter
from azureml.pipeline.steps import PythonScriptStep

# Define a pipeline parameter for the regularisation rate
reg_param = PipelineParameter(name="reg_rate", default_value=0.01)

(...)

# And use it in a pipeline task
step2 = PythonScriptStep(
    name = "train model",
    source_directory = "scripts",
    script_name = "data_prep.py",
    compute_target = "aml-cluster",
    # Pass parameter as script argument
    arguments=[
        "--in_folder", prepped_data,
        "--reg", reg_param
    ],
    inputs=[prepped_data]
)

# And the pipeline can be run with parameters as such (note the ParameterAssignments key)
response = requests.post(
    rest_endpoint,
    headers=auth_header,
    json={
        "ExperimentName": "run_training_pipeline",
        "ParameterAssignments": {"reg_rate": 0.1}
    }
)