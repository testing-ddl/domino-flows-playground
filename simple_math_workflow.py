
import os
from flytekit import workflow
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask, GitRef

# pyflyte run --remote simple_math_workflow.py simple_math_workflow --a 10 --b 6

@workflow
def simple_math_workflow(a: int, b: int) -> float:

    # Create first task 
    add_task = DominoJobTask(
        name='Add numbers',
        domino_job_config=DominoJobConfig(MainRepoGitRef=GitRef(Type="head"),Command="python add.py"),
        inputs={'first_value': int, 'second_value': int},
        outputs={'sum': int},
        use_latest=True
    )
    sum = add_task(first_value=a, second_value=b)

    # Create second task 
    sqrt_task = DominoJobTask(
        name='Square root',
        domino_job_config=DominoJobConfig(MainRepoGitRef=GitRef(Type="head"),Command="python sqrt.py"),
        inputs={'value': int},
        outputs={'sqrt': float},
        use_latest=True
    )
    sqrt = sqrt_task(value=sum)

    return sqrt