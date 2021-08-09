from azureml.pipeline.core import Schedule
from azureml.core import Datastore
from azureml.pipeline.core import ScheduleRecurrence, Schedule

# Run on schedule
##############################################################################
daily = ScheduleRecurrence(frequency="Day", interval=1)
pipeline_schedule = Schedule.create(
    ws,
    name="Daily Training",
    description="trains model every day",
    pipeline_id=published_pipeline.id,
    experiment_name="Training_Pipeline",
    recurrence=daily
)
##############################################################################


# Run on data change
##############################################################################

training_datastore = Datastore(workspace=ws, name="blob_data")
pipeline_schedule = Schedule.create(
    ws,
    name="Reactive Training",
    description="trains model on data change",
    pipeline_id=published_pipeline_id,
    experiment_name="Training_Pipeline",
    datastore=training_datastore,
    path_on_datastore="data/training"
)
##############################################################################
