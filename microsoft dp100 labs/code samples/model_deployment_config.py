from azureml.core.compute import ComputeTarget, AksCompute
from azureml.core.webservice import AksWebservice
from azureml.core import Workspace
from azureml.core.model import Model
from azureml.core.webservice import AksWebservice
from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.model import InferenceConfig

ws = Workspace.from_config()

# Add dependencies
myenv = CondaDependencies()
myenv.add_conda_package("scikit-learn")

# Save the environment config as a .yml file
env_file = 'service_files/env.yml'
with open(env_file,"w") as f:
    f.write(myenv.serialize_to_string())
print("Saved dependency info in", env_file)

# Create the Inference configuration
model_inference_config = InferenceConfig(
    runtime = "python",
    source_directory = 'service_files',
    entry_script = "your_entry_script.py",
    conda_file = "env.yml"
)

# This sample creates an AKS cluster for the compute
cluster_name = "aks-cluster"
compute_config = AksCompute.provisioning_configuration(location="eastus")
production_cluster = ComputeTarget.create(ws, cluster_name, compute_config)
production_cluster.wait_for_completion(show_output=True)
# Deployment configuration
model_deploy_config = AksWebservice.deploy_configuration(
    cpu_cores = 1,
    memory_gb = 1
)

# Deploy the model
model = ws.models["your_model"]
service = Model.deploy(
    workspace = ws,
    name = "service-name",
    models = [model],
    inference_config = model_inference_config,
    deployment_config = model_deploy_config,
    deployment_target = production_cluster
)
service.wait_for_deployment(show_output = True)

# Check the service state
print(service.state)

#########################
# Models can be deployed locally too
from azureml.core.webservice import LocalWebservice
deployment_config = LocalWebservice.deploy_configuration(port=8890)
service = Model.deploy(ws, "test-model", [model], model_inference_config, model_deploy_config)
# For changes in local files (local deployments only)
service.reload()