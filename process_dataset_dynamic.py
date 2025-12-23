#!/usr/bin/env python
"""
Script that receives dataset parameters from DominoJobTask inputs
and starts a nested Domino job with the dataset mounted using the API.

This works around Flyte's limitation by using Domino API directly.
"""

from pathlib import Path
import os
import sys
import json
import time

# Read dataset parameters from Flyte input files
# DominoJobTask writes inputs to /workflow/inputs/<input_name>
try:
    dataset_name = Path("/workflow/inputs/dataset_name").read_text().strip()
    dataset_id = Path("/workflow/inputs/dataset_id").read_text().strip()
    dataset_version = int(Path("/workflow/inputs/dataset_version").read_text().strip())
except FileNotFoundError as e:
    print(f"ERROR: Could not read input file: {e}")
    print("Available files in /workflow/inputs/:")
    if os.path.exists("/workflow/inputs"):
        for f in os.listdir("/workflow/inputs"):
            print(f"  - {f}")
    sys.exit(1)
except Exception as e:
    print(f"ERROR reading inputs: {e}")
    sys.exit(1)

print("=" * 80)
print("Dataset Parameters Received:")
print(f"  Name: {dataset_name}")
print(f"  ID: {dataset_id}")
print(f"  Version: {dataset_version}")
print("=" * 80)

# Get project information from environment
project_owner = os.environ.get("DOMINO_PROJECT_OWNER")
project_name = os.environ.get("DOMINO_PROJECT_NAME")
api_key = os.environ.get("DOMINO_USER_API_KEY")

if not all([project_owner, project_name]):
    print("ERROR: Missing DOMINO_PROJECT_OWNER or DOMINO_PROJECT_NAME")
    print("This script must run in a Domino environment")
    sys.exit(1)

print(f"\nProject: {project_owner}/{project_name}")

# Import Domino API
try:
    from domino import Domino
    domino = Domino(f"{project_owner}/{project_name}", api_key=api_key)
    print("✓ Domino API client initialized")
except ImportError:
    print("ERROR: domino-python package not installed")
    print("Install with: pip install dominodatalab")
    sys.exit(1)
except Exception as e:
    print(f"ERROR initializing Domino client: {e}")
    sys.exit(1)

# Start a nested Domino job with the dataset mounted
print(f"\nStarting nested Domino job with dataset {dataset_name} v{dataset_version}...")

try:
    # Command to run in the nested job
    command = f"echo 'Dataset: {dataset_name} v{dataset_version}' && ls -lR /mnt/data/{dataset_name}"

    # Start the job with runs_start (non-blocking)
    job_response = domino.runs_start(
        command=[command],
        isDirect=True,
        datasetSnapshotIds=[{
            "datasetId": dataset_id,
            "version": dataset_version
        }]
    )

    print(f"✓ Job started successfully")
    print(f"Response: {json.dumps(job_response, indent=2)}")

    # Get the run ID
    run_id = job_response.get('runId') or job_response.get('id')

    if run_id:
        print(f"\nMonitoring job: {run_id}")

        # Wait for job to complete
        max_wait = 300  # 5 minutes
        wait_interval = 5  # Check every 5 seconds
        elapsed = 0

        while elapsed < max_wait:
            status_info = domino.runs_status(run_id)
            status = status_info.get('status', 'Unknown')

            print(f"  Status: {status} (elapsed: {elapsed}s)")

            if status in ['Succeeded', 'Failed', 'Error', 'Stopped']:
                print(f"\n✓ Job completed with status: {status}")

                if status == 'Succeeded':
                    print("\n✓✓ Dataset job completed successfully!")
                    sys.exit(0)
                else:
                    print(f"\n✗ Job failed with status: {status}")
                    sys.exit(1)

            time.sleep(wait_interval)
            elapsed += wait_interval

        print(f"\n⚠ Job still running after {max_wait}s, but job was started successfully")
        sys.exit(0)
    else:
        print("WARNING: Could not get run ID from response, but job may have started")
        sys.exit(0)

except Exception as e:
    print(f"\nERROR starting nested job: {e}")
    print(f"Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
