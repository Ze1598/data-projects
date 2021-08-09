from azureml.core import Experiment, Workspace
import pandas as pd
import json
import os

# Connect to AML workspace
ws = Workspace.from_config()

# Create an experiment variable
experiment = Experiment(workspace = ws, name = "my-experiment")

# Start the experiment
run = experiment.start_logging()

# load the dataset and count the rows
data = pd.read_csv("data.csv")
row_count = (len(data))

# Log the row count
# The Run object is used to log named metrics for comparison across runs
run.log("observations", row_count)

# Upload a file to the outputs folder of the experiment
run.upload_file(name="outputs/sample.csv", path_or_stream="./sample.csv")

# Save a sample of the data (in the outputs folder)
os.makedirs("outputs", exist_ok=True)
data.sample(100).to_csv("outputs/sample.csv", index=False, header=True)


# End the experiment
run.complete()

# Get logged metrics for a run (in json format)
metrics = run.get_metrics()
print(json.dumps(metrics, indent=2))

# Get the output files of the model (includes uploaded files)
files = run.get_file_names()
print(json.dumps(files, indent=2))