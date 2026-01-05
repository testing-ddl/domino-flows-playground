from flytekit import workflow
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask, DatasetSnapshot


@workflow
def dataset_workflow_parameter(dataset_name: str, dataset_id: str, dataset_version: int):
    DominoJobTask(
        name='Process Dataset',
        domino_job_config=DominoJobConfig(
            Command="""python -c '
from pathlib import Path
import subprocess

name = Path("/workflow/inputs/dataset_name").read_text().strip()
ver = int(Path("/workflow/inputs/dataset_version").read_text().strip())

print(f"=== Dataset {name} Version {ver} ===")
result = subprocess.run(["ls", "-lR", f"/mnt/data/snapshots/{name}/{ver}"], capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print("Error:", result.stderr)
'
"""
        ),
        inputs={'dataset_name': str, 'dataset_id': str, 'dataset_version': int},
        use_latest=True,
    )(dataset_name=dataset_name, dataset_id=dataset_id, dataset_version=dataset_version)