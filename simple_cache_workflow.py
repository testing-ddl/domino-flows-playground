
import os
from flytekit import workflow
from flytekitplugins.domino.helpers import Input, Output, run_domino_job_task
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask, GitRef

# pyflyte run --remote simple_cache_workflow.py simple_cache_workflow --a 10

@workflow
def simple_cache_workflow(a: int) -> int:

    # Create first task 
    output1 = run_domino_job_task(
        flyte_task_name='Node 1',
        command="python pass_the_baton.py",
        main_git_repo_ref=GitRef(Type="commitId", Value="9fc19c5d95e4a21a5b677ce4ac7896d301d831b9"),
        environment_name="Domino Core Environment",
        hardware_tier_name="Small",
        inputs=[
            Input(name="input_value", type=int, value=a),
        ],
        output_specs=[
            Output(name="output_value", type=int)
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
    output2 = run_domino_job_task(
        flyte_task_name='Node 2',
        command="python pass_the_baton.py",
        main_git_repo_ref=GitRef(Type="commitId", Value="9fc19c5d95e4a21a5b677ce4ac7896d301d831b9"),
        environment_name="Domino Core Environment",
        hardware_tier_name="Small",
        inputs=[
            Input(name="input_value", type=int, value=output1),
        ],
        output_specs=[
            Output(name="output_value", type=int)
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

    # Create third task with different value 
    output3 = run_domino_job_task(
        flyte_task_name='Node 3',
        command="python pass_the_baton.py",
        main_git_repo_ref=GitRef(Type="commitId", Value="9fc19c5d95e4a21a5b677ce4ac7896d301d831b9"),
        environment_name="Domino Core Environment",
        hardware_tier_name="Small",
        inputs=[
            Input(name="input_value", type=int, value=output2),
        ],
        output_specs=[
            Output(name="output_value", type=int)
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

    return output3