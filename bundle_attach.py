"""Auto-attach flow artifact files to a governance bundle (e2e test flow).

Produces two artifact files and attaches them, on run completion, to the
bundle named ``QC Auto Attach Bundle`` in the same project. The bundle must
already exist in the project before this flow runs.

This file is meant to live in the domino-flows-playground repo so the cucu
test ``auto_attach_flow_artifact_files_to_bundle.feature`` can run it via:

    pyflyte run --remote bundle_attach.py bundle_attach
"""

from flytekit import task, workflow
from flytekit.types.file import FlyteFile

from flytekitplugins.domino.artifact import (
    MODEL,
    Artifact,
    ExportArtifactFilesToBundleSpec,
    run_launch_export_artifacts_task,
)

BUNDLE_NAME = "QC Auto Attach Bundle"

RiskModel = Artifact(name="risk-model", type=MODEL)
ModelFile = RiskModel.File(name="model.pkl")
MetricsFile = RiskModel.File(name="metrics.json")


@task
def produce_model() -> ModelFile:  # type: ignore[valid-type]
    path = "/tmp/model.pkl"
    with open(path, "wb") as f:
        f.write(b"mock model bytes")
    return FlyteFile(path)


@task
def produce_metrics() -> MetricsFile:  # type: ignore[valid-type]
    path = "/tmp/metrics.json"
    with open(path, "w") as f:
        f.write('{"accuracy": 0.97, "auc": 0.99}')
    return FlyteFile(path)


@workflow
def bundle_attach():
    produce_model()
    produce_metrics()

    run_launch_export_artifacts_task(
        spec_list=[
            ExportArtifactFilesToBundleSpec(
                files=[ModelFile, MetricsFile],
                bundles=[BUNDLE_NAME],
            ),
        ],
        use_project_defaults_for_omitted=True,
    )
