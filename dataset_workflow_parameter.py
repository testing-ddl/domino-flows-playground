import os
from flytekit import workflow
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask

# ==============================================================================
# TRULY DYNAMIC Dataset Workflow - Using Nested Job via Domino API
# ==============================================================================
# This workflow accepts dataset parameters at runtime and uses a nested Domino
# job approach to mount datasets dynamically.
#
# How it works:
# 1. Flyte workflow receives dataset parameters (name, ID, version)
# 2. Passes them to a DominoJobTask (no S3 issue because using inputs)
# 3. That job uses Domino API to start a NESTED job with the dataset mounted
# 4. The nested job actually has access to the dataset
#
# Usage:
#   pyflyte run --remote dataset_workflow_parameter.py dataset_workflow_parameter \
#     --dataset_name flows-gbp \
#     --dataset_id 66bfdc2ad58a430eb1d2a43a \
#     --dataset_version 1
#
#   pyflyte run --remote dataset_workflow_parameter.py dataset_workflow_parameter \
#     --dataset_name domino-flows-playground \
#     --dataset_id 6930e2ca5bb39a1e85b91c27 \
#     --dataset_version 1
# ==============================================================================


@workflow
def dataset_workflow_parameter(dataset_name: str, dataset_id: str, dataset_version: int):
    """
    Workflow that accepts ANY dataset parameters at runtime.

    This works by spinning up a nested Domino job via the API, which can
    accept dynamic dataset configurations.

    Args:
        dataset_name: Dataset name (e.g., "flows-gbp", "domino-flows-playground")
        dataset_id: Dataset ID (e.g., "66bfdc2ad58a430eb1d2a43a")
        dataset_version: Dataset version number (e.g., 1, 2, 3)
    """

    # Create a DominoJobTask that accepts dataset parameters as inputs
    # This task will start a nested Domino job with the dataset mounted
    process_dataset = DominoJobTask(
        name='Start Nested Job with Dataset',
        domino_job_config=DominoJobConfig(
            Command="python process_dataset_dynamic.py"
        ),
        inputs={
            'dataset_name': str,
            'dataset_id': str,
            'dataset_version': int
        },
        use_latest=True
    )

    # Execute the task with the provided parameters
    # This will start a nested job that has the dataset mounted
    process_dataset(
        dataset_name=dataset_name,
        dataset_id=dataset_id,
        dataset_version=dataset_version
    )