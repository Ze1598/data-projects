from azureml.core import Model, Workspace

# Connect to AML workspace
ws = Workspace.from_config()

# If the model already exists, then creates a new version
model = Model.register(
    workspace=ws,
    model_name="classification_model",
    model_path="model.pkl",  # local path
    description="A classification model",
    tags={"data-format": "CSV"},
    model_framework=Model.Framework.SCIKITLEARN,
    model_framework_version="0.20.3"
)

# View registered models
for model in Model.list(ws):
    # Get model name and auto-generated version
    print(model.name, 'version:', model.version)