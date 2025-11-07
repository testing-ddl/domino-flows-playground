from flytekit import workflow
from flytekit.types.file import FlyteFile
from flytekit.types.directory import FlyteDirectory
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask, GitRef
from flytekitplugins.domino.artifact import Artifact, DATA, MODEL, REPORT
from typing import TypeVar, Optional, List, Dict
import pandas as pd

ReportArtifact = Artifact(name="My Report", type=REPORT)
DataArtifact = Artifact(name="My Data", type=DATA)
ModelArtifact = Artifact(name="My Model", type=MODEL)

# pyflyte run --remote generate_artifacts.py generate_artifacts
@workflow
def generate_artifacts(): 

    sce_types = DominoJobTask(
        name="Generate SCE Types",
        domino_job_config=DominoJobConfig(MainRepoGitRef=GitRef(Type="head"),
                                          Command="python /mnt/code/scripts/generate-sce-types.py"),
        inputs={'sdtm_data_path': str},
        outputs={'pdf': ReportArtifact.File(name="generated.pdf"), 'sas7bdat': DataArtifact.File(name="data.sas7bdat")},
        use_latest=True
    )

    sce_types(sdtm_data_path="/mnt/code/artifacts")

    ml_types = DominoJobTask(
        name="Generate ML Types",
        domino_job_config=DominoJobConfig(MainRepoGitRef=GitRef(Type="head"),
                                          Command="python /mnt/code/scripts/generate-ml-types.py"),
        inputs={
            'batch_size': int,
            'learning_rate': float,
            'do_eval': bool,
            'list': List[int],
            'dict': Dict[str,int]
        },
        outputs={
            'csv': DataArtifact.File(name="data.csv"),
            'json': DataArtifact.File(name="data.json"),
            'png': ReportArtifact.File(name="report.png"),
            'jpeg': ReportArtifact.File(name="report.jpeg"),
            'notebook': DataArtifact.File(name="notebook.ipynb"),
            'pkl': ModelArtifact.File(name="intro.pkl"),
            'mlflow_model': FlyteDirectory
        },
        use_latest=True

    )

    ml_types(batch_size=32,
            learning_rate=0.001,
            do_eval=True,
            list=[1,2,3,4,5],
            dict={"param1": 1, "param2": 2,"param3": 3}
            )

    return 


@workflow
def generate_artifacts_with_dataset_exports(): 

    sce_types = DominoJobTask(
        name="Generate SCE Types",
        domino_job_config=DominoJobConfig(MainRepoGitRef=GitRef(Type="head"),
                                          Command="python /mnt/code/scripts/generate-sce-types.py"),
        inputs={'sdtm_data_path': str},
        outputs={'pdf': ReportArtifact.File(name="generated.pdf"), 'sas7bdat': DataArtifact.File(name="data.sas7bdat")},
        use_latest=True
    )

    sce_types(sdtm_data_path="/mnt/code/artifacts")

    from flytekitplugins.domino.artifact import run_launch_export_artifacts_task, ExportArtifactToDatasetsSpec
    run_launch_export_artifacts_task(
        spec_list=[
            ExportArtifactToDatasetsSpec(
                artifact=DataArtifact,
                dataset_id="DATASET_ID_TEMPLATE",
            ),
        ],
        use_project_defaults_for_omitted=True,
    )

    return 


@workflow
def generate_artifacts_with_netapp_volume_exports(): 

    sce_types = DominoJobTask(
        name="Generate SCE Types",
        domino_job_config=DominoJobConfig(MainRepoGitRef=GitRef(Type="head"),
                                          Command="python /mnt/code/scripts/generate-sce-types.py"),
        inputs={'sdtm_data_path': str},
        outputs={'pdf': ReportArtifact.File(name="generated.pdf"), 'sas7bdat': DataArtifact.File(name="data.sas7bdat")},
        use_latest=True
    )

    sce_types(sdtm_data_path="/mnt/code/artifacts")

    from flytekitplugins.domino.artifact import run_launch_export_artifacts_task, ExportArtifactToNetappVolumesSpec
    run_launch_export_artifacts_task(
        spec_list=[
            ExportArtifactToNetappVolumesSpec(
                artifact=DataArtifact,
                netapp_volume_id="NETAPP_VOLUME_ID_TEMPLATE",
            ),
        ],
        use_project_defaults_for_omitted=True,
    )

    return 


