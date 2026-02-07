from flytekit import workflow
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask


@workflow
def read_netapp_volume():
    """
    pyflyte run --remote neatapp_workflow_parameter.py read_netapp_volume
    
    Test workflow to verify NetApp volume mounting functionality in Flows.
    """
    DominoJobTask(
        name='read_netapp_volume',
        domino_job_config=DominoJobConfig(
            Command="""python -c '
from pathlib import Path
import os
import requests
import time

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
        "commandToRun": "ls -la /mnt/netapp && echo Volume contents: && find /mnt/netapp -type f -name \\\"*\\\" 2>/dev/null | head -20 || echo No files found in NetApp volumes",
        "isDirect": True
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
                print("\\n=== NetApp Volume Content ===")
                print("/mnt/netapp")
                print(stdout_resp.text)
            else:
                print(f"Could not fetch output (status {stdout_resp.status_code})")
        break
'
"""
        ),
        inputs={},
        use_latest=True,
    )()
