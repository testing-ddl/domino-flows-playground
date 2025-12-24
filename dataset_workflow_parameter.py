from flytekit import workflow
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask, DatasetSnapshot

@workflow
def dataset_workflow_parameter(dataset_name: str, dataset_id: str, dataset_version: int):
    DominoJobTask(
        name='Process Dataset',
        domino_job_config=DominoJobConfig(
            Command=f"ls -lR /mnt/data/{dataset_name}",
            DatasetSnapshots=[
                DatasetSnapshot(Id=dataset_id, Name=dataset_name, Version=dataset_version)
            ]
        ),
        use_latest=True,
    )()