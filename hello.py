
import os
from flytekit import workflow
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask, GitRef

@workflow
def hello_workflow(a: int, b: int) -> float:

    # Create first task 
    add_job = DominoJobTask(
        name='Add numbers',
        domino_job_config=DominoJobConfig(ApiKey=os.environ.get('DOMINO_USER_API_KEY'), MainRepoGitRef=GitRef(Type="head"),Command="python add.py"),
        inputs={'first_value': int, 'second_value': int},
        outputs={'sum': int},
        use_latest=True
    )
    sum = add_job(first_value=a, second_value=b)

    # Create second task 
    sqrt_job = DominoJobTask(
        name='Square root',
        domino_job_config=DominoJobConfig(
            ApiKey=os.environ.get('DOMINO_USER_API_KEY'),
            MainRepoGitRef=GitRef(Type="head"),
            Command="python sqrt.py"
        ),
        inputs={'value': int},
        outputs={'sqrt': float},
        use_latest=True
    )
    sqrt = sqrt_job(value=sum)
    
    return sqrt
