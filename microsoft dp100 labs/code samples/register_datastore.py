from azureml.core import Workspace, Datastore

ws = Workspace.from_config()

# Register a new datastore
blob_ds = Datastore.register_azure_blob_container(
    workspace=ws, 
    datastore_name="blob_data", 
    container_name="data_container",
    account_name="az_store_acct",
    account_key="123456abcde789…"
)

# Get registered datastores
for ds_name in ws.datastores:
    print(ds_name)

# Get a single datastore
some_datastore = Datastore.get(ws, datastore_name="your_datastore")

# Get the workspace's default datastore (workspaceblobstore)
default_store = ws.get_default_datastore()

# Change default datastore
ws.set_default_datastore("your_datastore")