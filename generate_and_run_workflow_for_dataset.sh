sed "s/DATASET_ID_TEMPLATE/$1/g" generate_artifacts.py > generate_artifacts_with_dataset_exports.py
pyflyte run --remote generate_artifacts_with_dataset_exports.py generate_artifacts_with_dataset_exports
