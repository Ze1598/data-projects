from azureml.core import Workspace

# Connect to AML workspace
ws = Workspace.from_config()

# Get each compute target available in the workspace
for compute_name in ws.compute_targets:
    compute = ws.compute_targets[compute_name]
    print(compute.name, ":", compute.type)


# Bash alternative
# -g: resource group
# -w: workspace
# az ml computetarget list -g 'aml-resources' -w 'aml-workspace'