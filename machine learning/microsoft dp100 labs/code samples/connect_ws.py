from azureml.core import Workspace

# Requires config.json file, path can be specified
ws = Workspace.from_config()

# Or the configurations can be specified individually
ws = Workspace.get(
    name="aml-workspace",
    subscription_id="1234567-abcde-890-fgh...",
    resource_group="aml-resources"
)