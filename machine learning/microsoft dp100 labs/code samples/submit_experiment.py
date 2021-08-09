from azureml.core import Workspace, Experiment, ScriptRunConfig

# Connect to AML workspace
ws = Workspace.from_config()

# Create a script config
# Any dependencies (e.g. data files) must be in the same folder
# And required libraries must also be imported in the script
script_config = ScriptRunConfig(
    source_directory = "experiment_files",
    script = "experiment.py"
) 

# Submit the experiment
experiment = Experiment(workspace = ws, name = "my-experiment")
run = experiment.submit(config = script_config)
run.wait_for_completion(show_output = True)