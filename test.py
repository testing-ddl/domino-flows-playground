from utils.flyte import DominoTask, Input, Output
from flytekit import workflow, dynamic
from flytekit.experimental import eager
from flytekit.types.file import FlyteFile
from flytekit.types.directory import FlyteDirectory
from typing import TypeVar, Optional
import pandas as pd
import os
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask, GitRef, EnvironmentRevisionSpecification, EnvironmentRevisionType, DatasetSnapshot
from domino import Domino


# pyflyte run --remote test.py test_workflow
@eager
def dynamic_flow(commit_id: str): 
    api_key=os.environ.get('DOMINO_USER_API_KEY')
    job_config = DominoJobConfig(
        Title="Test job",
        ApiKey=api_key,
        Command="sleep 100",
        MainRepoGitRef=GitRef(Type="commitId", Value=commit_id), 
        HardwareTierId="Small",
        VolumeSizeGiB=10
    )
    job_config.resolve_job_properties()
    job = DominoJobTask(
        "Test job",
        job_config,
    )
    job()
    return 

@workflow
def test_workflow(commit_id: str):
    dynamic_flow(commit_id=commit_id)
    return
