from flytekitplugins.domino.helpers import Input, Output, run_domino_job_task
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask, GitRef, EnvironmentRevisionSpecification, EnvironmentRevisionType, DatasetSnapshot
from flytekit import workflow
from flytekitplugins.domino.file import DominoFile, DominoFileLegacy
from flytekit.types.directory import FlyteDirectory
from flytekit.types.file import FlyteFile
from typing import TypeVar, NamedTuple

final_outputs = NamedTuple("final_outputs", model=DominoFile)

@workflow
def training_workflow(data_path: str) -> final_outputs: 
    """
    Sample data preparation and training workflow
    This workflow accepts a path to a CSV for some initial input and simulates
    the processing of the data and usage of the processed data in a training job.
    To run this workflow, execute the following line in the terminal
    pyflyte run --remote paths-wf.py training_workflow --data_path /mnt/code/artifacts/data.csv
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
            Output(name="processed_data", type=DominoFile[TypeVar("csv")])
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
            Input(name="processed_data_domino_file", type=DominoFile[TypeVar("csv")], value=data_prep_results['processed_data']),
            Input(name="processed_data_flyte_file", type=FlyteFile[TypeVar("csv")], value=data_prep_results['processed_data']),
            Input(name="processed_data_domino_file_legacy", type=DominoFileLegacy[TypeVar("csv")], value=data_prep_results['processed_data']),
            Input(name="epochs", type=int, value=10),
            Input(name="batch_size", type=int, value=32)
        ],
        output_specs=[
            Output(name="model", type=DominoFile)
        ],
        use_project_defaults_for_omitted=True,
        cache=True,
        cache_version="1.0"
    )

    return final_outputs(model=training_results['model'])
