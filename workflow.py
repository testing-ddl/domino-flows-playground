# from utils.flyte import DominoTask, Input, Output
from flytekit import workflow
from flytekit.types.file import FlyteFile
from flytekit.types.directory import FlyteDirectory
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask, GitRef
from typing import TypeVar, Optional, List, Dict
import pandas as pd

@workflow
def training_workflow(data_path: str) -> FlyteFile: 
    """
    Sample data preparation and training workflow

    This workflow accepts a path to a CSV for some initial input and simulates
    the processing of the data and usage of the processed data in a training job.

    To run this workflowp, execute the following line in the terminal

    pyflyte run --remote workflow.py training_workflow --data_path /mnt/code/artifacts/data.csv

    :param data_path: Path of the CSV file data
    :return: The training results as a model
    """

    data_prep_results = DominoJobTask(
        name="Prepare data",
        domino_job_config=DominoJobConfig(MainRepoGitRef=GitRef(Type="head"),
                                          Command="python /mnt/code/scripts/prep-data.py"),
        # environment="Data Prep Environment",
        # hardware_tier="Small",
        inputs={'data_path': str},
        outputs={'processed_data': FlyteFile},
        use_latest=True
    )

    processed_data = data_prep_results(data_path=data_path)

    training_results = DominoJobTask(
        name="Train model",
        domino_job_config=DominoJobConfig(MainRepoGitRef=GitRef(Type="head"),
                                          Command="python/mnt/code/scripts/train-model.py"),
        # environment="Training Environment",
        # hardware_tier="Medium",
        inputs={'processed_data': FlyteFile, 'epochs': int, 'batch_size': int},
        outputs={'model': FlyteFile},
        use_latest=True
    )

    return training_results(processed_data=processed_data, epochs = 10, batch_size = 32)

@workflow
def training_subworkflow(data_path: str) -> FlyteFile: 

    data_prep_results = DominoJobTask(
        name="Prepare data",
        domino_job_config=DominoJobConfig(MainRepoGitRef=GitRef(Type="head"),Command="python /mnt/code/scripts/prep-data.py"),
        # environment="Data Prep Environment",
        # hardware_tier="Small",
        inputs={'data_path': str},
        outputs={'processed_data': FlyteFile},
        use_latest=True
    )

    processed_data = data_prep_results(data_path=data_path)

    training_results = DominoJobTask(
        name="Train model",
        domino_job_config=DominoJobConfig(MainRepoGitRef=GitRef(Type="head"),
                                          Command="python/mnt/code/scripts/train-model.py"),
        # environment="Training Environment",
        # hardware_tier="Medium",
        inputs={'processed_data': FlyteFile, 'epochs': int, 'batch_size': int},
        outputs={'model': FlyteFile},
        use_latest=True
    )

    return training_results(processed_data=processed_data, epochs = 10, batch_size = 32)

# pyflyte run --remote workflow.py generate_types 
@workflow
def generate_types(): 

    sce_types = DominoJobTask(
        name="Generate SCE Types",
        domino_job_config=DominoJobConfig(MainRepoGitRef=GitRef(Type="head"),
                                          Command="python /mnt/code/scripts/generate-sce-types.py"),
        # environment="Domino Standard Environment Py3.9 R4.3",
        # hardware_tier="Small",
        inputs={'sdtm_data_path': str},
        outputs={'pdf':FlyteFile[TypeVar("pdf")], 'sas7bdat': FlyteFile[TypeVar("sas7bdat")]},
        use_latest=True
    )

    sce_types(sdtm_data_path="/mnt/code/artifacts")

    ml_types = DominoJobTask(
        name="Generate ML Types",
        domino_job_config=DominoJobConfig(MainRepoGitRef=GitRef(Type="head"),
                                          Command="python /mnt/code/scripts/generate-ml-types.py"),
        inputs={
            'batch_size': int,
            'learning_rate': float,
            'do_eval': bool,
            'list': List[int],
            'dict': Dict[str,int]
        },
        outputs={
            'csv': FlyteFile[TypeVar("csv")],
            'json': FlyteFile[TypeVar("json")],
            'png': FlyteFile[TypeVar("csv")],
            'jpeg': FlyteFile[TypeVar("jpeg")],
            'notebook': FlyteFile[TypeVar("ipynb")],
            'mlflow_model': FlyteDirectory
        },
        use_latest=True

    )

    ml_types(batch_size=32,
            learning_rate=0.001,
            do_eval=True,
            list=[1,2,3,4,5],
            dict={"param1": 1, "param2": 2,"param3": 3}
            )

    return 

# pyflyte run --remote workflow.py training_workflow --data_path /mnt/code/artifacts/data.csv
@workflow
def training_workflow_git(data_path: str) -> FlyteFile: 
    """
    Sample data preparation and training workflow

    This workflow accepts a path to a CSV for some initial input and simulates
    the processing of the data and usage of the processed data in a training job.

    To run this workflow, execute the following line in the terminal

    pyflyte run --remote workflow.py training_workflow --data_path /mnt/code/artifacts/data.csv

    :param data_path: Path of the CSV file data
    :return: The training results as a model
    """

    data_prep_results = DominoJobTask(
        name="Prepare data ",
        domino_job_config=DominoJobConfig(MainRepoGitRef=GitRef(Type="head"),Command="python /mnt/code/scripts/prep-data.py"),
        inputs={'data_path': str},
        outputs={'processed_data': FlyteFile},
        use_latest=True
    )

    processed_data = data_prep_results(data_path=data_path)

    training_results = DominoJobTask(
        name="Train model ",
        domino_job_config=DominoJobConfig(MainRepoGitRef=GitRef(Type="head"),
                                          Command="python /mnt/code/scripts/train-model.py"),
        # environment="Training Environment",
        # hardware_tier="Medium",
        inputs={'processed_data': FlyteFile, 'epochs': int, 'batch_size': int},
        outputs={'model': FlyteFile},
        use_latest=True
    )

    return training_results(processed_data=processed_data, epochs = 10, batch_size = 32)

# pyflyte run --remote workflow.py training_workflow_nested --data_path /mnt/code/artifacts/data.csv
@workflow
def training_workflow_nested(data_path: str): 

    model = training_subworkflow(data_path=data_path)

    results = DominoJobTask(
        name="Final task",
        domino_job_config=DominoJobConfig(MainRepoGitRef=GitRef(Type="head"),Command="sleep 100"),
        # environment="Training Environment",
        # hardware_tier="Medium",
        inputs={'model': FlyteFile},
        use_latest=True
            # Input(name="model", type=FlyteFile, value=model)
    )

    return 


# pyflyte run --remote workflow.py training_workflow_mlflow
@workflow
def training_workflow_mlflow():
    """
    Sample mlflow training workflow

    To run this workflow, execute the following line in the terminal

    pyflyte run --remote workflow.py training_workflow_mlflow
    """

    data_prep_results = DominoJobTask(
        name="Run experiment",
        domino_job_config=DominoJobConfig(MainRepoGitRef=GitRef(Type="head"),
                                          Command="python /mnt/code/scripts/experiment.py"),
        use_latest=True
        # environment="Training Environment",
        # hardware_tier="Medium",
    )

    return