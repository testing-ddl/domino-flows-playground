
import os
from flytekit import workflow
from flytekitplugins.domino.helpers import Input, Output, run_domino_job_task
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask, GitRef

# pyflyte run --remote simple_math_cache_workflow.py simple_math_workflow --a 10 --b 6

@workflow
def simple_math_workflow(a: int, b: int) -> float:

    # Create first task 
    sum = add_task = run_domino_job_task(
        flyte_task_name='Add numbers',
        command="python add.py",
        main_git_repo_ref=GitRef(Type="commitId", Value="9fc19c5d95e4a21a5b677ce4ac7896d301d831b9"),
        environment_name="Domino Core Environment",
        hardware_tier_name="Small",
        # domino_job_config=DominoJobConfig(MainRepoGitRef=GitRef(Type="head"),Command="python add.py"),
        inputs=[
            Input(name="first_value", type=int, value=a),
            Input(name="second_value", type=int, value=b)
        ],
        output_specs=[
            Output(name="sum", type=int)
        ],
        # inputs={'first_value': int, 'second_value': int},
        # outputs={'sum': int},
        cache=True,
        cache_version="1.0",

        # flyte_task_name="Prepare data",
        # command="python /mnt/code/scripts/prep-data.py",
        # main_git_repo_ref=GitRef(Type="commitId", Value="9fc19c5d95e4a21a5b677ce4ac7896d301d831b9"),
        # environment_name="Domino Core Environment",
        # hardware_tier_name="Small",
        # inputs=[
        #     Input(name="data_path", type=str, value=data_path)
        # ],
        # output_specs=[
        #     Output(name="processed_data", type=FlyteFile[TypeVar("csv")])
        # ],
        use_project_defaults_for_omitted=True,
        
    )
    # sum = add_task(first_value=a, second_value=b)

    # Create second task 
    sqrt = sqrt_task = run_domino_job_task(
        flyte_task_name='Square root',
        command="python sqrt.py",
        main_git_repo_ref=GitRef(Type="commitId", Value="9fc19c5d95e4a21a5b677ce4ac7896d301d831b9"),
        environment_name="Domino Core Environment",
        hardware_tier_name="Small",
        # domino_job_config=DominoJobConfig(MainRepoGitRef=GitRef(Type="head"),Command="python sqrt.py"),
        inputs=[
            Input(name="value", type=int, value=sum)
        ],
        output_specs=[
            Output(name="sqrt", type=float)
        ],
        # inputs={'value': int},
        # outputs={'sqrt': float},
        use_project_defaults_for_omitted=True,
        cache=True,
        cache_version="1.0"
    )
    # sqrt = sqrt_task(value=sum)

    return sqrt