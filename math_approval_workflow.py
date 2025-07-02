from flytekit import approve, workflow
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask
from datetime import timedelta

# pyflyte run --remote math_approval_workflow.py approval_flow --a 10 --b 6

@workflow
def approval_flow(a: int, b: int) -> float:

    # Create first task
    add_task = DominoJobTask(
        name='Add numbers',
        domino_job_config=DominoJobConfig(Command="python add.py"),
        inputs={'first_value': int, 'second_value': int},
        outputs={'sum': int},
        use_latest=True
    )

    # Approval is added here
    sum = approve(add_task(first_value=a, second_value=b), "Approval", timeout=timedelta(hours=2))

    # Create second task
    sqrt_task = DominoJobTask(
        name='Square root',
        domino_job_config=DominoJobConfig(Command="python sqrt.py"),
        inputs={'value': int},
        outputs={'sqrt': float},
        use_latest=True
    )
    sqrt = sqrt_task(value=sum)

    return sqrt