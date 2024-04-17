from flytekit import CronSchedule, LaunchPlan 
from workflow import training_workflow

# creates a launch plan that runs every minute.
cron_lp = LaunchPlan.get_or_create(
    name="scheduled_training_workflow",
    workflow=training_workflow,
    default_inputs={"data_path": "/mnt/code/artifacts/data.csv"},
    schedule=CronSchedule(
        schedule="*/1 * * * *",  # Following schedule runs every min
        kickoff_time_input_arg="data_path"
    )
)