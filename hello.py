import os
from typing import List
from flytekit import workflow
from flytekit.types.file import FlyteFile
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask, GitRef, EnvironmentRevisionSpecification, EnvironmentRevisionType, DatasetSnapshot
from flytekit.loggers import logger
from dataclasses import dataclass
from domino import Domino

@workflow
def hello_workflow(a: int, b: int) -> float:

    # Create first task 
    add_job_config = DominoJobConfig(
        ApiKey=os.environ.get('DOMINO_USER_API_KEY'),
        Title='Add numbers',
        MainRepoGitRef=GitRef(Type="head"),
        Command="python add.py"
    )
    add_job_config.resolve_job_properties()
    add_job = DominoJobTask(
        'Add numbers',
        add_job_config,
        inputs={'first_value': int, 'second_value': int},
        outputs={'sum': int}
    )
    sum = add_job(first_value=a, second_value=b)

    # Create second task 
    sqrt_job_config = DominoJobConfig(
        ApiKey=os.environ.get('DOMINO_USER_API_KEY'),
        Title='Square root',
        MainRepoGitRef=GitRef(Type="head"),
        Command="python sqrt.py"
    )
    sqrt_job_config.resolve_job_properties()
    sqrt_job = DominoJobTask(
        'Square root',
        sqrt_job_config,
        inputs={'value': int},
        outputs={'sqrt': float}
    )
    sqrt = sqrt_job(value=sum)
    return sqrt
