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
import time

name = Path("/workflow/inputs/dataset_name").read_text().strip()
did = Path("/workflow/inputs/dataset_id").read_text().strip()
ver = int(Path("/workflow/inputs/dataset_version").read_text().strip())

project_id = os.environ["DOMINO_PROJECT_ID"]
api_key = os.environ["DOMINO_USER_API_KEY"]
api_host = os.environ["DOMINO_API_HOST"]
owner = os.environ["DOMINO_PROJECT_OWNER"]
project = os.environ["DOMINO_PROJECT_NAME"]
headers = {"X-Domino-Api-Key": api_key, "Content-Type": "application/json"}

response = requests.post(
    f"{api_host}/v4/jobs/start",
    headers=headers,
    json={
        "projectId": project_id,
        "commandToRun": f"ls -lR /mnt/data/snapshots/{name}/{ver}",
        "isDirect": True,
        "datasetSnapshotReferences": [{"datasetId": did, "version": ver}]
    }
)

job_id = response.json().get("id")

for i in range(60):
    time.sleep(2)
    status_resp = requests.get(f"{api_host}/v4/jobs/{job_id}", headers=headers)
    job_data = status_resp.json()
    status = job_data.get("statuses", {}).get("executionStatus")
    if status in ["Succeeded", "Failed", "Error"]:
        output_commit_id = job_data.get("commitDetails", {}).get("outputCommitId")
        if output_commit_id:
            stdout_url = f"{api_host}/u/{owner}/{project}/render/results/stdout.txt?commitId={output_commit_id}"
            stdout_resp = requests.get(stdout_url, headers=headers)
            if stdout_resp.status_code == 200:
                print(f"\\n=== Dataset {name} Version {ver} ===")
                print(stdout_resp.text)
            else:
                print(f"Could not fetch output (status {stdout_resp.status_code})")
        break
'
"""
        ),
        inputs={'dataset_name': str, 'dataset_id': str, 'dataset_version': int},
        use_latest=True,
    )(dataset_name=dataset_name, dataset_id=dataset_id, dataset_version=dataset_version)