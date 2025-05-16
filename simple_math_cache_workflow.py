
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
        inputs=[
            Input(name="first_value", type=int, value=a),
            Input(name="second_value", type=int, value=b)
        ],
        output_specs=[
            Output(name="sum", type=int)
        ],
        cache=True,
        cache_version="1.0",
        external_data_volumes=[],
        dataset_snapshots=[],
        volume_size_gib=10,

        # Minumum usage of use defaults
        use_project_defaults_for_omitted=True,
        # dfs_repo_commit_id="",
        # environment_revision_id=""
    )

    # Create second task 
    sqrt = sqrt_task = run_domino_job_task(
        flyte_task_name='Square root',
        command="python sqrt.py",
        main_git_repo_ref=GitRef(Type="commitId", Value="9fc19c5d95e4a21a5b677ce4ac7896d301d831b9"),
        environment_name="Domino Core Environment",
        hardware_tier_name="Small",
        inputs=[
            Input(name="value", type=int, value=sum)
        ],
        output_specs=[
            Output(name="sqrt", type=float)
        ],
        cache=True,
        cache_version="1.0",
        external_data_volumes=[],
        dataset_snapshots=[],
        volume_size_gib=10,
        
        # Minumum usage of use defaults
        use_project_defaults_for_omitted=True,
        # dfs_repo_commit_id="",
        # environment_revision_id=""
    )

    return sqrt