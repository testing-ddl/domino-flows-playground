
import os
from flytekit import workflow
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask, GitRef, DatasetSnapshot

# This test code assumes a project name of flows-gbp

# pyflyte run --remote dataset_workflow_parameter.py dataset_workflow_parameter --datasetName flows-gbp --datasetId 66bfdc2ad58a430eb1d2a43a --datasetVersion 1

@workflow
def dataset_workflow_parameter(datasetName: str, datasetId: str, datasetVersion: int):

 DominoJobTask(
     name="My dataset workflow",
     domino_job_config=DominoJobConfig(
         Command=f"ls -lR /mnt/data/{datasetName}",
         DatasetSnapshots=[
             DatasetSnapshot(Id=datasetId, Name=datasetName, Version=datasetVersion),
         ],
     ),
     use_latest=True,
 )()