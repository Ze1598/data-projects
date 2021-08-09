from azureml.core import Workspace, Experiment, ScriptRunConfig, Environment
from azureml.core.conda_dependencies import CondaDependencies

# Create a Python environment for the experiment
sklearn_env = Environment("sklearn-env")

# Ensure the required packages are installed
packages = CondaDependencies.create(
    conda_packages=["scikit-learn","pip"],
    pip_packages=["azureml-defaults"]
)
sklearn_env.python.conda_dependencies = packages

# Connect to AML workspace
ws = Workspace.from_config()

# Create a script config
script_config = ScriptRunConfig(
    source_directory="training_folder",
    script="training.py",
    # Here
    arguments = ["--reg-rate", 0.1],
    environment=sklearn_env
)

# Submit the experiment
experiment = Experiment(workspace = ws, name = "my-experiment")
run = experiment.submit(config = script_config)
run.wait_for_completion(show_output = True)