from flytekit import workflow
from flytekitplugins.domino.file import DominoFile
from flytekit.types.directory import FlyteDirectory
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask, GitRef
from typing import TypeVar, Optional, List, Dict
import pandas as pd

# pyflyte run --remote generate_files.py generate_types 
@workflow
def generate_types(): 

    sce_types = DominoJobTask(
        name="Generate SCE Types",
        domino_job_config=DominoJobConfig(MainRepoGitRef=GitRef(Type="head"),
                                          Command="python /mnt/code/scripts/generate-sce-types.py"),
        inputs={'sdtm_data_path': str},
        outputs={'pdf':DominoFile[TypeVar("pdf")], 'sas7bdat': DominoFile[TypeVar("sas7bdat")]},
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
            'csv': DominoFile[TypeVar("csv")],
            'json': DominoFile[TypeVar("json")],
            'png': DominoFile[TypeVar("png")],
            'jpeg': DominoFile[TypeVar("jpeg")],
            'notebook': DominoFile[TypeVar("ipynb")],
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

# pyflyte run --remote generate_files.py generate_types_on_remote_hw_tier 
@workflow
def generate_types_on_remote_hw_tier(): 

    sce_types = DominoJobTask(
        name="Generate SCE Types",
        domino_job_config=DominoJobConfig(MainRepoGitRef=GitRef(Type="head"),
                                          Command="python /mnt/code/scripts/generate-sce-types.py",
                                          HardwareTierId="small-k8s-remote"
                                          ),
        inputs={'sdtm_data_path': str},
        outputs={'pdf':DominoFile[TypeVar("pdf")], 'sas7bdat': DominoFile[TypeVar("sas7bdat")]},
        use_latest=True
    )

    sce_types(sdtm_data_path="/mnt/code/artifacts")

    ml_types = DominoJobTask(
        name="Generate ML Types",
        domino_job_config=DominoJobConfig(MainRepoGitRef=GitRef(Type="head"),
                                          Command="python /mnt/code/scripts/generate-ml-types.py",
                                          HardwareTierId="small-k8s-remote"
                                          ),
        inputs={
            'batch_size': int,
            'learning_rate': float,
            'do_eval': bool,
            'list': List[int],
            'dict': Dict[str,int]
        },
        outputs={
            'csv': DominoFile[TypeVar("csv")],
            'json': DominoFile[TypeVar("json")],
            'png': DominoFile[TypeVar("png")],
            'jpeg': DominoFile[TypeVar("jpeg")],
            'notebook': DominoFile[TypeVar("ipynb")],
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
