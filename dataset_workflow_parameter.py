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
import requests

name = Path("/workflow/inputs/dataset_name").read_text().strip()
did = Path("/workflow/inputs/dataset_id").read_text().strip()
ver = int(Path("/workflow/inputs/dataset_version").read_text().strip())

owner = os.environ["DOMINO_PROJECT_OWNER"]
project = os.environ["DOMINO_PROJECT_NAME"]
api_key = os.environ.get("DOMINO_USER_API_KEY")
api_host = os.environ.get("DOMINO_API_HOST", "https://sushant100409.engineering-sandbox.domino.tech")

url = f"{api_host}/v4/jobs/start"
headers = {"X-Domino-Api-Key": api_key, "Content-Type": "application/json"}

payload = {
    "projectId": f"{owner}/{project}",
    "command": f"ls -lR /mnt/data/{name}",
    "isDirect": True,
    "datasetSnapshotReferences": [{
        "datasetId": did,
        "version": ver
    }]
}

response = requests.post(url, headers=headers, json=payload)
result = response.json()
print(f"Job started: {json.dumps(result, indent=2)}")
'
"""
        ),
        inputs={'dataset_name': str, 'dataset_id': str, 'dataset_version': int},
        use_latest=True,
    )(dataset_name=dataset_name, dataset_id=dataset_id, dataset_version=dataset_version)