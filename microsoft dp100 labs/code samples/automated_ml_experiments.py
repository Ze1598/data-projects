from azureml.train.automl import AutoMLConfig
from azureml.core.experiment import Experiment

automl_run_config = RunConfiguration(framework="python")
automl_config = AutoMLConfig(
    name="Automated ML Experiment",
    task="classification",
    primary_metric="AUC_weighted",
    compute_target=aml_compute,
    training_data=train_dataset,
    validation_data=test_dataset,
    label_column_name="Label",
    featurization="auto",
    iterations=12,
    max_concurrent_iterations=4
)


automl_experiment = Experiment(ws, "automl_experiment")
# Submit the auto ml experiment as any other experiment
automl_run = automl_experiment.submit(automl_config)

# Get best run and its model
best_run, fitted_model = automl_run.get_output()
best_run_metrics = best_run.get_metrics()
for metric_name in best_run_metrics:
    metric = best_run_metrics[metric_name]
    print(metric_name, metric)

# Get pre-processing steps used
for step_ in fitted_model.named_steps:
    print(step_)