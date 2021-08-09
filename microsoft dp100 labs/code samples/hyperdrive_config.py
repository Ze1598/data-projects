from azureml.core import Experiment
from azureml.train.hyperdrive import HyperDriveConfig, PrimaryMetricGoal


# The training script must:
# include an argument for each hyperparameter you want to vary;
# log the target performance metric. This enables the hyperdrive run to evaluate the performance of the child runs it initiates, and identify the one that produces the best performing model.

hyperdrive = HyperDriveConfig(
    run_config=your_run_config_obj,
    hyperparameter_sampling=your_param_sampling,
    policy=None,
    primary_metric_name="your_metric",
    primary_metric_goal=PrimaryMetricGoal.MAXIMIZE,
    max_total_runs=6,
    max_concurrent_runs=4
)

experiment = Experiment(workspace = ws, name = "hyperdrive_training")
hyperdrive_run = experiment.submit(config=hyperdrive)


# And to review the runs
# All runs in order of execution
for child_run in hyperdrive_run.get_children():
    print(child_run.id, child_run.get_metrics())
# All runs sorted in descending order of performance
for child_run in hyperdrive_run.get_children_sorted_by_primary_metric():
    print(child_run)
# Best run
best_run = hyperdrive_run.get_best_run_by_primary_metric()