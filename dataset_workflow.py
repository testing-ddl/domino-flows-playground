
import os
from flytekit import workflow
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask, GitRef, DatasetSnapshot

# This test code assumes a project name of flows-gbp

# pyflyte run --remote dataset_workflow.py dataset_workflow

@workflow
def dataset_workflow():

 DominoJobTask(
     name="My dataset workflow",
     domino_job_config=DominoJobConfig(
         Command="ls -lR /mnt/data/flows-gbp",
         DatasetSnapshots=[
             DatasetSnapshot(Id="66bfdc2ad58a430eb1d2a43a", Name="flows-gbp", Version=1),
             # DatasetSnapshot(Id="66bfdc2ad58a430eb1d2a43a", Name="flows-gbp", Version=2),
         ],
     ),
     use_latest=True,
 )()