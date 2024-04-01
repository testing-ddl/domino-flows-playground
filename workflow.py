from utils.flyte import run_domino_job, Input, Output
from flytekit import workflow
from flytekit.types.file import FlyteFile
from flytekit.types.directory import FlyteDirectory

@workflow
def training_workflow(data_path: FlyteFile) -> FlyteFile: 
    """
    Sample data preparation and training workflow

    This workflow accepts a path to a CSV for some initial input and simulates
    the processing of the data and usage of the processed data in a training job.

    To run this workflowp, execute the following line in the terminal

    pyflyte run --remote workflow.py training_workflow --data_path /mnt/code/data/data.csv

    :param data_path: Path of the CSV file data
    :return: The training results as a model
    """

    data_prep_results = run_domino_job(
        name="Prepare data",
        environment="Data Prep Environment",
        hardware_tier="Small",
        command="python /mnt/code/scripts/prep-data.py",
        inputs=[
            Input(name="data_path", type=FlyteFile, value=data_path)
        ],
        outputs=[
            Output(name="processed_data", type=FlyteFile)
        ]
    )

    training_results = run_domino_job(
        name="Train model",
        environment="Training Environment",
        hardware_tier="Medium",
        command="python /mnt/code/scripts/train-model.py",
        inputs=[
            Input(name="processed_data", type=FlyteFile, value=data_prep_results['processed_data']),
            Input(name="epochs", type=int, value=10),
            Input(name="batch_size", type=int, value=32)
        ],
        outputs=[
            Output(name="model", type=FlyteFile)
        ]
    )

    return training_results['model']
