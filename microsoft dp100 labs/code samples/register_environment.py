from azureml.core import Environment, Workspace, ScriptRunConfig
from azureml.core.conda_dependencies import CondaDependencies

# Get workspace
ws = Workspace.from_config()

# Create conda env from yml file
env = Environment.from_conda_specification(
    name="training_environment",
    file_path="./conda.yml"
)

# Create conda env from existing conda env
env = Environment.from_existing_conda_environment(
    name="training_environment",
    conda_environment_name="py_env"
)

# Create conda env from scratch
env = Environment("training_environment")
deps = CondaDependencies.create(
    conda_packages=["scikit-learn","pandas","numpy"],
    pip_packages=["azureml-defaults"]
)
env.python.conda_dependencies = deps

# Register env in workspace
env.register(workspace=ws)

# Get all existing envs
env_names = Environment.list(workspace=ws)
for env_name in env_names:
    print("Name:",env_name)


# Get specific env and use it
training_env = Environment.get(
    workspace=ws, 
    name="training_environment")
script_config = ScriptRunConfig(
    source_directory="my_dir",
    script="script.py",
    environment=training_env
)