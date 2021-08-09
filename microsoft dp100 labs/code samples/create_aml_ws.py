from azureml.core import Workspace

ws = Workspace.create(
    name="aml-workspace",
    subscription_id="123456-abc-123...",
    resource_group="aml-resources",
    create_resource_group=True,
    location="eastus"
)


# Bash alternative
# az ml workspace create -w 'aml-workspace' -g 'aml-resources'