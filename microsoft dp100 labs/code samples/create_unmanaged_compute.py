from azureml.core import Workspace
from azureml.core.compute import ComputeTarget, DatabricksCompute
from azureml.core.compute_target import ComputeTargetException
from azureml.core import Environment, ScriptRunConfig

# Load the workspace from the saved config file
ws = Workspace.from_config()

# Specify a name for the compute (unique within the workspace)
compute_name = "db_cluster"

# Check if the compute target exists
try:
    aml_cluster = ComputeTarget(workspace=ws, name=compute_name)
    print('Found existing cluster.')
    
except ComputeTargetException:
    # Define configuration for existing Azure Databricks cluster
    db_workspace_name = "db_workspace"
    db_resource_group = "db_resource_group"
    db_access_token = "1234-abc-5678-defg-90..."
    db_config = DatabricksCompute.attach_configuration(
        resource_group=db_resource_group,
        workspace_name=db_workspace_name,
        access_token=db_access_token
    )

    # Create the compute
    databricks_compute = ComputeTarget.attach(ws, compute_name, db_config)

databricks_compute.wait_for_completion(True)


# And now use the compute target
training_env = Environment.get(workspace=ws, name="training_environment")
script_config = ScriptRunConfig(
    source_directory = "my_dir",
    script = "script.py",
    environment = training_env,
    compute_target = compute_name
    # or compute_target = databricks_compute
)