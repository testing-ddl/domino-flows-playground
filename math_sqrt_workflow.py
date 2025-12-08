
import os
from flytekit import workflow
from utils.flyte import DominoTask, Input, Output
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask, GitRef
from flytekitplugins.domino.helpers import Input, Output, run_domino_job_task

# pyflyte run --remote simple_sqrt_workflow.py simple_sqrt_workflow --a 10 --b 6

@workflow
def simple_sqrt_workflow(a: int, b: int) -> float:
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

