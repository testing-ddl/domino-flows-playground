from flytekit import workflow
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask, DatasetSnapshot


@workflow
def dataset_workflow_parameter(dataset_name: str, dataset_id: str, dataset_version: int):
    DominoJobTask(
        name='Process Dataset',
        domino_job_config=DominoJobConfig(
            Command="""python -c '
from pathlib import Path
import os
import requests
import json

name = Path("/workflow/inputs/dataset_name").read_text().strip()
did = Path("/workflow/inputs/dataset_id").read_text().strip()
ver = int(Path("/workflow/inputs/dataset_version").read_text().strip())

print(f"Dataset: {name}, ID: {did}, Version: {ver}")

api_key = os.environ.get("DOMINO_USER_API_KEY")
api_host = os.environ.get("DOMINO_API_HOST", "https://sushant100409.engineering-sandbox.domino.tech")

url = f"{api_host}/v4/jobs/start"
headers = {"X-Domino-Api-Key": api_key, "Content-Type": "application/json"}

payload = {
    "commandToRun": [f"ls -lR /mnt/data/{name}"],
    "isDirect": True,
    "datasetSnapshotReferences": [
        {"datasetId": did, "version": ver}
    ]
}

print(f"Calling API: {url}")
print(f"Payload: {json.dumps(payload, indent=2)}")

response = requests.post(url, headers=headers, json=payload)
print(f"Response status: {response.status_code}")
print(f"Response: {response.text}")
'
"""
        ),
        inputs={'dataset_name': str, 'dataset_id': str, 'dataset_version': int},
        use_latest=True,
    )(dataset_name=dataset_name, dataset_id=dataset_id, dataset_version=dataset_version)