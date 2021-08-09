from azureml.core import Workspace

ws = Workspace.from_config()
# Get Application Insights resource associated with this workspace
ws.get_details()["applicationInsights"]

...
# Enable Application Insights for a new real-time service with `enable_app_insights`

dep_config = AciWebservice.deploy_configuration(
    cpu_cores = 1,
    memory_gb = 1,
    enable_app_insights=True
)

...
# Enable Application Insights for an already existing service

service = ws.webservices["my-service"]
service.update(enable_app_insights=True)

... 
# Capture service telemetry in the service's scoring script

def init():
    global model
    model = joblib.load(Model.get_model_path('my_model'))
def run(raw_data):
    data = json.loads(raw_data)['data']
    predictions = model.predict(data)
    log_txt = f"Data: {str(data)} - Predictions: {str(predictions)}"
    # Print calls are enough
    print(log_txt)
    return predictions.tolist()

...

# Query the logs through Log Analytics in Application Insights, in Azure Portal

traces
|where message == "STDOUT"
  and customDimensions.["Service Name"] = "my-svc"
| project  timestamp, customDimensions.Content
