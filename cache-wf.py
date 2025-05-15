from flytekitplugins.domino.helpers import Input, Output, run_domino_job_task
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask, GitRef, EnvironmentRevisionSpecification, EnvironmentRevisionType, DatasetSnapshot
from flytekit import workflow
from flytekit.types.file import FlyteFile
from flytekit.types.directory import FlyteDirectory
from typing import TypeVar, NamedTuple

final_outputs = NamedTuple("final_outputs", model=FlyteFile)

@workflow
def training_workflow(data_path: str) -> final_outputs: 
    """
    Sample data preparation and training workflow
    This workflow accepts a path to a CSV for some initial input and simulates
    the processing of the data and usage of the processed data in a training job.
    To run this workflowp, execute the following line in the terminal
    pyflyte run --remote cache-wf.py training_workflow --data_path /mnt/code/artifacts/data.csv
    :param data_path: Path of the CSV file data
    :return: The training results as a model
    """

    data_prep_results = run_domino_job_task(
        flyte_task_name="Prepare data",
        command="python /mnt/code/scripts/prep-data.py",
        environment_name="Domino Core Environment",
        # environment_name="Domino Standard Environment Py3.10 R4.4",
        hardware_tier_name="Small",
        inputs=[
            Input(name="data_path", type=str, value=data_path)
        ],
        output_specs=[
            Output(name="processed_data", type=FlyteFile[TypeVar("csv")])
        ],
        use_project_defaults_for_omitted=True,
        cache=True,
        cache_version="1.0"
    )

    training_results = run_domino_job_task(
        flyte_task_name="Train model",
        command="python /mnt/code/scripts/train-model.py",
        environment_name="Domino Core Environment",
        # environment_name="Domino Standard Environment Py3.10 R4.4",
        hardware_tier_name="Small",
        inputs=[
            Input(name="processed_data", type=FlyteFile[TypeVar("csv")], value=data_prep_results['processed_data']),
            Input(name="epochs", type=int, value=10),
            Input(name="batch_size", type=int, value=32)
        ],
        output_specs=[
            Output(name="model", type=FlyteFile)
        ],
        use_project_defaults_for_omitted=True,
        cache=True,
        cache_version="1.0"
    )

    return final_outputs(model=training_results['model'])

@workflow
def training_workflow_cache(data_path: str) -> final_outputs: 
    """
    Sample data preparation and training workflow
    This workflow accepts a path to a CSV for some initial input and simulates
    the processing of the data and usage of the processed data in a training job.
    To run this workflowp, execute the following line in the terminal
    pyflyte run --remote cache-wf.py training_workflow_cache --data_path /mnt/code/artifacts/data.csv
    :param data_path: Path of the CSV file data
    :return: The training results as a model
    """
    
    data_prep_results = run_domino_job_task(
        flyte_task_name="Prepare data",
        command="python /mnt/code/scripts/prep-data.py",
        main_git_repo_ref=GitRef(Type="commitId", Value="9fc19c5d95e4a21a5b677ce4ac7896d301d831b9"),
        environment_name="Domino Core Environment",
        hardware_tier_name="Small",
        inputs=[
            Input(name="data_path", type=str, value=data_path)
        ],
        output_specs=[
            Output(name="processed_data", type=FlyteFile[TypeVar("csv")])
        ],
        use_project_defaults_for_omitted=True,
        cache=True,
        cache_version="1.0"
    )

    training_results = run_domino_job_task(
        flyte_task_name="Train model",
        command="python /mnt/code/scripts/train-model.py",
        environment_name="Domino Core Environment",
        main_git_repo_ref=GitRef(Type="commitId", Value="9fc19c5d95e4a21a5b677ce4ac7896d301d831b9"),
        hardware_tier_name="Small",
        inputs=[
            Input(name="processed_data", type=FlyteFile[TypeVar("csv")], value=data_prep_results['processed_data']),
            Input(name="epochs", type=int, value=10),
            Input(name="batch_size", type=int, value=32)
        ],
        output_specs=[
            Output(name="model", type=FlyteFile)
        ],
        use_project_defaults_for_omitted=True,
        cache=True,
        cache_version="1.0"
    )

    return final_outputs(model=training_results['model'])