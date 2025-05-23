"""
Helper script to run generate_artifacts.generate_artifacts_with_dataset_exports with the specified dataset.
The script parses the dataset id from the input dataset URL, and creates a new workflow file with this dataset
id injected into it via sed.
"""
DATASET_ID=$(basename "$1")
sed "s/DATASET_ID_TEMPLATE/$DATASET_ID/g" generate_artifacts.py > generate_artifacts_with_dataset_exports.py
pyflyte run --remote generate_artifacts_with_dataset_exports.py generate_artifacts_with_dataset_exports
