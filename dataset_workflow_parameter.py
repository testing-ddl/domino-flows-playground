from flytekit import workflow
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask


@workflow
def dataset_workflow_parameter(dataset_name: str, dataset_id: str, dataset_version: int):
    DominoJobTask(
        name='Process Dataset',
        domino_job_config=DominoJobConfig(
            Command="""python -c '
from pathlib import Path
import os
import json
from domino import Domino

name = Path("/workflow/inputs/dataset_name").read_text().strip()
did = Path("/workflow/inputs/dataset_id").read_text().strip()
ver = int(Path("/workflow/inputs/dataset_version").read_text().strip())

owner = os.environ["DOMINO_PROJECT_OWNER"]
project = os.environ["DOMINO_PROJECT_NAME"]
domino = Domino(f"{owner}/{project}")

cmd = f"ls -lR /mnt/data/{name}"

try:
    job = domino.job_start(
        command=cmd,
        datasetIds=[did]
    )
    print(f"Job started with dataset: {json.dumps(job, indent=2)}")
except TypeError:
    job = domino.runs_start(command=[cmd], isDirect=True)
    print(f"Job started (no dataset API support): {json.dumps(job, indent=2)}")
'
"""
        ),
        inputs={'dataset_name': str, 'dataset_id': str, 'dataset_version': int},
        use_latest=True,
    )(dataset_name=dataset_name, dataset_id=dataset_id, dataset_version=dataset_version)