
import os
from flytekit import workflow
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask, GitRef, DatasetSnapshot

# This test code assumes a project name of flows-gbp

# pyflyte run --remote dataset_workflow_parameter.py dataset_workflow_parameter --name flows-gbp --id 66bfdc2ad58a430eb1d2a43a --version 1

@workflow
def dataset_workflow_parameter(name: str, id: str, version: int):
 cmd = f"ls -lR /mnt/data/{name}"
 DominoJobTask(
     name="My dataset workflow",
     domino_job_config=DominoJobConfig(
         Command=cmd,
         DatasetSnapshots=[
             DatasetSnapshot(Id=id, Name=name, Version=version),
         ],
     ),
     use_latest=True,
 )()