from flytekit import workflow
from flytekit.types.file import FlyteFile
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
        outputs={'pdf':FlyteFile[TypeVar("pdf")], 'sas7bdat': FlyteFile[TypeVar("sas7bdat")]},
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
            'csv': FlyteFile[TypeVar("csv")],
            'json': FlyteFile[TypeVar("json")],
            'png': FlyteFile[TypeVar("csv")],
            'jpeg': FlyteFile[TypeVar("jpeg")],
            'notebook': FlyteFile[TypeVar("ipynb")],
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