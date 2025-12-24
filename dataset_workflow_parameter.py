from flytekit import workflow
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask

# Dynamic Dataset Workflow - All in one file, no external scripts needed
# Usage: pyflyte run --remote dataset_dynamic.py wf --dataset_name <name> --dataset_id <id> --dataset_version <ver>


@workflow
def wf(dataset_name: str, dataset_id: str, dataset_version: int):
    """Dynamic dataset workflow - accepts any dataset at runtime"""

    DominoJobTask(
        name='Process Dataset',
        domino_job_config=DominoJobConfig(
            Command=f"""python -c "
from pathlib import Path
import os
from domino import Domino

# Read inputs from Flyte
name = Path('/workflow/inputs/dataset_name').read_text().strip()
dataset_id = Path('/workflow/inputs/dataset_id').read_text().strip()
ver = int(Path('/workflow/inputs/dataset_version').read_text().strip())

print('=' * 80)
print(f'Dataset: {{name}} (ID: {{dataset_id}}, Version: {{ver}})')
print('=' * 80)

# Initialize Domino client
owner = os.environ['DOMINO_PROJECT_OWNER']
project = os.environ['DOMINO_PROJECT_NAME']
domino = Domino(f'{{owner}}/{{project}}')

# Start nested job with dataset via API
cmd = f'echo Processing {{name}} v{{ver}} && ls -lR /mnt/data/{{name}}'

print(f'Starting nested job...')
print(f'Command: {{cmd}}')

try:
    job = domino.runs_start(command=[cmd], isDirect=True)
    job_id = job.get(\\'runId\\') or job.get(\\'id\\')
    print(f'✓ Job started: {{job_id}}')
except Exception as e:
    print(f'Error: {{e}}')
    raise
"
"""
        ),
        inputs={'dataset_name': str, 'dataset_id': str, 'dataset_version': int},
        use_latest=True,
    )(dataset_name=dataset_name, dataset_id=dataset_id, dataset_version=dataset_version)
