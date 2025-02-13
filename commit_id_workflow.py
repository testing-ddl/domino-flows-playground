
import os
from flytekit import workflow
from utils.flyte import DominoTask, Input, Output
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask, GitRef
from flytekitplugins.domino.helpers import Input, Output, run_domino_job_task

# pyflyte run --remote different_execution_parameters.py simple_math_workflow --a 10 --b 6

@workflow
def simple_math_workflow(a: int, b: int) -> float:

    add_task = run_domino_job_task(
        flyte_task_name="Add numbers",
        command="python add.py",
        main_git_repo_ref=GitRef(type="commitId", value="99a3b59788e681e066f21780569eeb0ad6b05cdb")
        environment_name="Domino Standard Environment Py3.10 R4.4",
        hardware_tier_name="Small",
        inputs=[
            Input(name="first_value", type=int, value=a),
            Input(name="second_value", type=int, value=b)
        ],
        output_specs=[
            Output(name="sum", type=int)
        ],
        use_project_defaults_for_omitted=True,
    )
    sum = add_task['sum']

    sqrt_task = run_domino_job_task(
        flyte_task_name="Square root",
        command="python sqrt.py",
        environment_name="Domino Core Environment",
        hardware_tier_name="Medium",
        inputs=[
            Input(name="value", type=int, value=sum)
        ],
        output_specs=[
            Output(name="sqrt", type=float)
        ],
        use_project_defaults_for_omitted=True,
    )
    sqrt = sqrt_task['sqrt']

    return sqrt

