from typing import TypeVar
from flytekitplugins.domino.helpers import Output, run_domino_job_task
from flytekitplugins.domino.artifact import Artifact, MODEL
from flytekit import workflow
from flytekit.types.file import FlyteFile

ModelArtifact = Artifact("My Model", MODEL)

# pyflyte run --remote model_artifact.py single_model

@workflow
def single_model() -> ModelArtifact.File(name="model.pkl"):
    return run_domino_job_task(
        flyte_task_name="Produce model",
        command="produce_model.py",
        output_specs=[
            # name of the Output can differ from the name of the ArtifactFile
            Output(name="my_model", type=FlyteFile[TypeVar("pkl")]),
        ],
        use_project_defaults_for_omitted=True,
    )