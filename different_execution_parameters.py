
import os
from flytekit import workflow
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask, GitRef

# pyflyte run --remote different_execution_parameters.py simple_math_workflow --a 10 --b 6

@workflow
def simple_math_workflow(a: int, b: int) -> float:

    # Create first task 
    add_task = DominoJobTask(
        name='Add numbers',
        domino_job_config=DominoJobConfig(
            MainRepoGitRef=GitRef(Type="head"),
            Command="python add.py",
            HardwareTierId="small",
            EnvironmentId="670ea2296223a55666316652"
        ),
        inputs={'first_value': int, 'second_value': int},
        outputs={'sum': int},
        use_latest=True
    )
    sum = add_task(first_value=a, second_value=b)

    # Create second task 
    sqrt_task = DominoJobTask(
        name='Square root',
        domino_job_config=DominoJobConfig(
            MainRepoGitRef=GitRef(Type="head"),
            Command="python sqrt.py",
            HardwareTierId="medium",
            EnvironmentId="670ea2296223a5566631664c"
        ),
        inputs={'value': int},
        outputs={'sqrt': float},
        use_latest=True
    )
    sqrt = sqrt_task(value=sum)

    return sqrt