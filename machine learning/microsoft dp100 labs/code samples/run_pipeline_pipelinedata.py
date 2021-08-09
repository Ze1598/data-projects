from azureml.core import Workspace, Dataset
from azureml.pipeline.core import PipelineData
from azureml.pipeline.steps import PythonScriptStep

ws = Workspace.from_config()

# Define pipeline stepts
###############################################################################
# Get a dataset for the initial data
raw_ds = Dataset.get_by_name(ws, "raw_dataset")

# Define a PipelineData object to pass data between steps
data_store = ws.get_default_datastore()
prepped_data = PipelineData("prepped",  datastore=data_store)

# Step to run a Python script for preparing data
step1 = PythonScriptStep(
    name="prepare data",
    source_directory="scripts",
    script_name="data_prep.py",
    compute_target="aml-cluster",
    # Script arguments include PipelineData
    arguments=[
        "--raw-ds", raw_ds.as_named_input("raw_data"),
        "--out_folder", prepped_data
    ],
    # Specify PipelineData as output
    outputs=[prepped_data]
)

# Step to run a Python script for training the model
step2 = PythonScriptStep(
    name="train model",
    source_directory="scripts",
    script_name="data_train.py",
    compute_target="aml-cluster",
    # Pass as script argument
    arguments=["--in_folder", prepped_data],
    # Specify PipelineData as input
    inputs=[prepped_data]
)
###############################################################################


# And in the script being executed (e.g. for the first PythonScriptStep task)
###############################################################################
# code in data_prep.py
from azureml.core import Run
import argparse
import os

# Get the experiment run context
run = Run.get_context()

# Get arguments
parser = argparse.ArgumentParser()
parser.add_argument("--raw-ds", type=str, dest="raw_dataset_id")
# This will read a PipelineData object, but it can be treated as a reference to a datastore
parser.add_argument("--out_folder", type=str, dest="folder")
args = parser.parse_args()
output_folder = args.folder

# Get input dataset as dataframe
# it was defined with `as_named_input("raw_data")`
raw_df = run.input_datasets["raw_data"].to_pandas_dataframe()

# code to prep data (in this case, just select specific columns)
prepped_df = raw_df[["col1", "col2", "col3"]]

# Save prepped data to the PipelineData location
os.makedirs(output_folder, exist_ok=True)
output_path = os.path.join(output_folder, "prepped_data.csv")
prepped_df.to_csv(output_path)
###############################################################################