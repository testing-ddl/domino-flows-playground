from utils.flyte import DominoTask, Input, Output
from flytekit import workflow
from flytekit.types.file import FlyteFile
from flytekit.types.directory import FlyteDirectory
import pandas as pd

@workflow
def training_workflow(data_path: str) -> FlyteFile: 
    """
    Sample data preparation and training workflow

    This workflow accepts a path to a CSV for some initial input and simulates
    the processing of the data and usage of the processed data in a training job.

    To run this workflowp, execute the following line in the terminal

    pyflyte run --remote workflow.py training_workflow --data_path /mnt/code/data/data.csv

    :param data_path: Path of the CSV file data
    :return: The training results as a model
    """

    data_prep_results = DominoTask(
        name="Prepare data",
        command="python /mnt/code/scripts/prep-data.py",
        environment="Data Prep Environment",
        hardware_tier="Small",
        inputs=[
            Input(name="data_path", type=str, value=data_path)
        ],
        outputs=[
            Output(name="processed_data", type=FlyteFile)
        ]
    )

    training_results = DominoTask(
        name="Train model",
        command="python /mnt/code/scripts/train-model.py",
        environment="Training Environment",
        hardware_tier="Medium",
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

# pyflyte run --remote workflow.py generate_types 
@workflow
def generate_types(): 

    sce_types = DominoTask(
        name="Generate SCE Types",
        command="python /mnt/code/scripts/generate-sce-types.py",
        environment="Domino Standard Environment Py3.9 R4.3",
        hardware_tier="Small",
        inputs=[
            Input(name="sdtm_data_path", type=str, value="/some/path/to/data")
        ],
        outputs=[
            Output(name="pdf", type=FlyteFile),
            Output(name="sas7bdat", type=FlyteFile)
        ]
    )

    ml_types = DominoTask(
        name="Generate ML Types",
        command="python /mnt/code/scripts/generate-ml-types.py",
        environment="Domino Standard Environment Py3.9 R4.3",
        hardware_tier="Small",
        inputs=[
            Input(name="batch_size", type=int, value=32),
            Input(name="learning_rate", type=float, value=0.001),
            Input(name="do_eval", type=bool, value=True),
        ],
        outputs=[
            Output(name="csv", type=FlyteFile),
            Output(name="json", type=FlyteFile),
            Output(name="png", type=FlyteFile),
            Output(name="jpeg", type=FlyteFile),
            Output(name="notebook", type=FlyteFile),
            Output(name="mlflow_model", type=FlyteDirectory)
        ]
    )

    return 

