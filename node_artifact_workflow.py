from flytekit import workflow
from flytekitplugins.domino.file import DominoFile
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask
from flytekitplugins.domino.artifact import Artifact, DATA, MODEL, REPORT
from typing import TypeVar, NamedTuple

# may use any name and the type DATA, MODEL or REPORT
DataArtifact = Artifact(name='Study Data', type=DATA)
ReportArtifact = Artifact(name='Official Report', type=REPORT)

final_outputs = NamedTuple(
    'final_outputs',
    report_html=ReportArtifact.File(name='final.html'),
    report_graph=ReportArtifact.File(name='final.png'),
)

# pyflyte run --remote node_artifact_workflow.py clean_and_prep_data
@workflow
def clean_and_prep_data() -> final_outputs: 
    # simulate a job that retrieves data
    raw = DominoJobTask(
        name='Retrieve raw data',
        domino_job_config=DominoJobConfig(Command='python data.py'),
        inputs={'rows': int, 'cols': int},
        outputs={'data': DataArtifact.File(name='raw.csv')},
        use_latest=True
    )(rows=20, cols=10)

    # simulate cleaning the raw data
    clean = DominoJobTask(
        name='Clean raw data',
        domino_job_config=DominoJobConfig(Command='python clean.py'),
        inputs={'data': DominoFile[TypeVar('csv')]},
        outputs={'data': DataArtifact.File(name='clean.csv')},
        use_latest=True
    )(data=raw.data)

    # take the output data from the clean job
    generate_report = DominoJobTask(
        name='Render data as an official report',
        domino_job_config=DominoJobConfig(Command='python report.py'),
        inputs={'data': DominoFile[TypeVar('csv')]},
        outputs={
            'html': DominoFile[TypeVar('html')],
            'graph': DominoFile[TypeVar('png')]
        },
        use_latest=True
    )(data=clean.data)

    return final_outputs(generate_report.html, generate_report.graph) 