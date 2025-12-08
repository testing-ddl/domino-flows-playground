
import os
from flytekit import workflow
from utils.flyte import DominoTask, Input, Output
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask, GitRef
from flytekitplugins.domino.helpers import Input, Output, run_domino_job_task

# pyflyte run --remote simple_sum_workflow.py simple_sum_workflow --a 10 --b 6

@workflow
def simple_sum_workflow(a: int, b: int) -> float:
    # Create first task 
    add_job = DominoJobTask(
        name='Add numbers',
        domino_job_config=DominoJobConfig(Command="python add.py"),
        inputs={'first_value': int, 'second_value': int},
        outputs={'sum': int},
        use_latest=True
    )
    sum = add_job(first_value=a, second_value=b)

    return sum
