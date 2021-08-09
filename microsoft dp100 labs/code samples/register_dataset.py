from azureml.core import Workspace, Dataset

# Get workspace
ws = Workspace.from_config()
# Get default datastore
blob_ds = ws.get_default_datastore()

# Register a tabular dataset using csv files from two directories
csv_paths = [
    (blob_ds, "data/files/current_data.csv"),
    (blob_ds, "data/files/archive/*.csv")
]
tab_ds = Dataset.Tabular.from_delimited_files(path=csv_paths)
tab_ds = tab_ds.register(workspace=ws, name="csv_table")

# Register a file dataset that includes all jpg files in the directory
file_ds = Dataset.File.from_files(
    path = (blob_ds, "data/files/images/*.jpg")
)
file_ds = file_ds.register(workspace=ws, name="img_files")



# Get a dataset from the workspace datasets collection
ds1 = ws.datasets["csv_table"]
# Get a dataset by name from the datasets class
ds2 = Dataset.get_by_name(ws, "img_files")


# Register a new dataset version
img_paths = [
    (blob_ds, "data/files/images/*.jpg"),
    (blob_ds, "data/files/images/*.png")
]
file_ds = Dataset.File.from_files(path=img_paths)
file_ds = file_ds.register(workspace=ws, name="img_files", create_new_version=True)


# Get a specific dataset version
img_ds = Dataset.get_by_name(workspace=ws, name="img_files", version=2)