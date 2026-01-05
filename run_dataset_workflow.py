#!/usr/bin/env python
"""
Direct script to list dataset contents without nested jobs.
Usage: python run_dataset_workflow.py <dataset_name> <dataset_id> <dataset_version>
"""
import sys
import os
import requests
import time

if len(sys.argv) != 4:
    print("Usage: python run_dataset_workflow.py <dataset_name> <dataset_id> <dataset_version>")
    sys.exit(1)

name = sys.argv[1]
did = sys.argv[2]
ver = int(sys.argv[3])

project_id = os.environ.get("DOMINO_PROJECT_ID")
api_key = os.environ.get("DOMINO_USER_API_KEY")
api_host = os.environ.get("DOMINO_API_HOST")
owner = os.environ.get("DOMINO_PROJECT_OWNER")
project = os.environ.get("DOMINO_PROJECT_NAME")

if not all([project_id, api_key, owner, project]):
    print("Error: Missing required environment variables")
    sys.exit(1)

headers = {"X-Domino-Api-Key": api_key, "Content-Type": "application/json"}

print(f"Starting job to list dataset: {name} (version {ver})")

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
print(f"Job ID: {job_id}")

print("Waiting for job to complete...")
for i in range(60):
    time.sleep(2)
    status_resp = requests.get(f"{api_host}/v4/jobs/{job_id}", headers=headers)
    job_data = status_resp.json()
    status = job_data.get("statuses", {}).get("executionStatus")
    if status in ["Succeeded", "Failed", "Error"]:
        output_commit_id = job_data.get("commitDetails", {}).get("outputCommitId")
        if output_commit_id and status == "Succeeded":
            stdout_url = f"{api_host}/u/{owner}/{project}/render/results/stdout.txt?commitId={output_commit_id}"
            stdout_resp = requests.get(stdout_url, headers=headers)
            if stdout_resp.status_code == 200:
                print(f"\n=== Dataset {name} Version {ver} ===")
                print(stdout_resp.text)
            else:
                print(f"Could not fetch output (status {stdout_resp.status_code})")
        elif status == "Failed":
            print(f"Job failed. View details at: {api_host}/jobs/{job_id}")
        break
