
import os
from flytekit import workflow
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask, GitRef, DatasetSnapshot

# This test code assumes a project name of flows-gbp

# pyflyte run --remote dataset_workflow_parameter.py dataset_workflow_parameter --name flows-gbp --id 66bfdc2ad58a430eb1d2a43a --version 1

# pyflyte run --remote dataset_workflow_parameter.py dataset_workflow_parameter --name domino-flows-playground --id  --version 1

@workflow
def dataset_workflow_parameter():
 DominoJobTask(
     name="My dataset workflow",
     domino_job_config=DominoJobConfig(
         Command="ls -lR /mnt/data/domino-flows-playground",
         DatasetSnapshots=[
             DatasetSnapshot(Id="694ad96631428063c406a0a9", Name="domino-flows-playground", Version=1),
         ],
     ),
     use_latest=True,
 )()