from azureml.core import Workspace
from azureml.core.compute import ComputeTarget, AmlCompute
from azureml.core.compute_target import ComputeTargetException
from azureml.core import Environment, ScriptRunConfig

# Load the workspace from the saved config file
ws = Workspace.from_config()

# Specify a name for the compute (unique within the workspace)
compute_name = "aml-cluster"

# Check if the compute target exists
try:
    aml_cluster = ComputeTarget(workspace=ws, name=compute_name)
    print("Found existing cluster.")

except ComputeTargetException:
    # Define compute configuration
    compute_config = AmlCompute.provisioning_configuration(
        vm_size="STANDARD_DS11_V2",
        min_nodes=0, 
        max_nodes=4,
        vm_priority="dedicated"
    )
    
    # Create the compute
    aml_cluster = ComputeTarget.create(ws, compute_name, compute_config)
    aml_cluster.wait_for_completion(show_output=True)

aml_cluster.wait_for_completion(show_output=True)

# And now use the compute target
training_env = Environment.get(workspace=ws, name="training_environment")
script_config = ScriptRunConfig(
    source_directory = "my_dir",
    script = "script.py",
    environment = training_env,
    compute_target = compute_name
    # or compute_target = aml_cluster
)