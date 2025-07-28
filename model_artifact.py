from flytekit import workflow
from flytekit.types.file import FlyteFile
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask
from flytekitplugins.domino.artifact import Artifact, DATA, MODEL, REPORT
from typing import TypeVar, NamedTuple

# define the artifact name and type which may be REPORT, DATA or MODEL
DataArtifact = Artifact(name="My Data", type=DATA)
ModelArtifact = Artifact(name="My Model", type=MODEL)

# pyflyte run --remote model_artifact.py training_workflow --data_path /mnt/code/artifacts

@workflow
def training_workflow(data_path: str) -> ModelArtifact.File(name="model.pt"):

    data_prep_job_config = DominoJobConfig(Command="python prep-data.py")
    data_prep_job = DominoJobTask(
        name='Prep data',
        domino_job_config=data_prep_job_config,
        inputs={'data_path': str},
        outputs={'processed_data': DataArtifact.File(name="data.csv")},
        use_latest=True
    )
    data_prep_results = data_prep_job(data_path=data_path)

    training_job_config = DominoJobConfig(Command="python train-model.py")
    training_job = DominoJobTask(
        name='Train model',
        domino_job_config=training_job_config,
        inputs={'processed_data': FlyteFile[TypeVar("csv")]},
        outputs={'model': FlyteFile[TypeVar("pt")]},
        use_latest=True
    )
    training_results = training_job(processed_data=data_prep_results["processed_data"])

    return training_results["model"] # Final output is returned here