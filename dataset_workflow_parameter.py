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
import requests

name = Path("/workflow/inputs/dataset_name").read_text().strip()
did = Path("/workflow/inputs/dataset_id").read_text().strip()
ver = int(Path("/workflow/inputs/dataset_version").read_text().strip())

project_id = os.environ["DOMINO_PROJECT_ID"]
api_key = os.environ["DOMINO_USER_API_KEY"]
api_host = os.environ["DOMINO_API_HOST"]

response = requests.post(
    f"{api_host}/v4/jobs/start",
    headers={"X-Domino-Api-Key": api_key, "Content-Type": "application/json"},
    json={
        "projectId": project_id,
        "commandToRun": f"ls -lR /mnt/data/{name}",
        "isDirect": True,
        "datasetSnapshotReferences": [{"datasetId": did, "version": ver}]
    }
)

result = response.json()
job_id = result.get("id")
print(f"Dataset {name} v{ver} - Job started: {job_id} - response: {result}")
'
"""
        ),
        inputs={'dataset_name': str, 'dataset_id': str, 'dataset_version': int},
        use_latest=True,
    )(dataset_name=dataset_name, dataset_id=dataset_id, dataset_version=dataset_version)