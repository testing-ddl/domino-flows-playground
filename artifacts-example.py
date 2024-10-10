from flytekitplugins.domino.helpers import DominoJobTask, DominoJobConfig, Input, Output
from flytekit import workflow, dynamic
from flytekit.types.file import FlyteFile
from flytekit.types.directory import FlyteDirectory
from typing import TypeVar, Optional, List, Dict, Annotated, Tuple, NamedTuple
from flytekit import Artifact
import uuid

# key pieces of data to collect

# artifact groups are identified uniquely within an execution by composite key
# * name
# * type

# artifact files within each group are identified uniquely by filename and graph node
# * filename
# * graph node
# * artifact group (foreign key)
# NOTE: there is an edge case where different outputs in the same node could be annotated identically - we'll require validation to prevent this

# the problem is the way that Flyte stores metadata and how the existing development experience works
# it makes it cumbersome to place artifacts into specific groups b/c of how the Python types are defined

# we need to change the DX because:
# it's error prone
# requires specifying the group values as partitions again and again
# requires more code than should be necessary, including predefining Artifacts by name instead of inside the Annotation
# the name of the artifact should be able to automatically set the extension (used by frontend for file previews)

# also note its worth investigating behavior dynamic partitions - i.e. ReportArtifact.create_from()

# upstream code here shows some examples
# https://github.com/flyteorg/flytekit/blob/master/flytekit/core/artifact.py#L371
# https://github.com/flyteorg/flytekit/blob/master/tests/flytekit/unit/core/test_artifacts.py

# to use partition_keys (necessary for Domino), we have to define this type up front -- this entire definition should be eliminated
ReportArtifact = Artifact(name="report.pdf", partition_keys=["type", "group"])
ReportArtifact2 = Artifact(name="report2.pdf", partition_keys=["type", "group"])
ReportArtifact3 = Artifact(name="report3.pdf", partition_keys=["type", "group"])

# ideally, a group is defined like this
# ReportGroup = Group(name="my custom report", type=Report)

@workflow
def artifact_meta(data_path: str) -> Tuple[
    Annotated[FlyteFile, ReportArtifact(type="report", group="report_foo")], 
    Annotated[FlyteFile, ReportArtifact2(type="report", group="report_foo")], 
    Annotated[FlyteFile, ReportArtifact3(type="report", group="report_bar")], 

    # ideally the definition looks more like this:
    # Annotated[FlyteFile, Artifact(name="report.pdf", Group=ReportGroup)], 
    # this could be further simplified in the programming model if we know that these artifacts are only a single file like
    # ArtifactFile(name="report.pdf", Group=ReportGroup)

    # normal workflow output with no annotations
    FlyteFile
    ]: 
    """py
    pyflyte run --remote artifacts-example.py artifact_meta --data_path /mnt/data.csv
    """

    data_prep_results = DominoJobTask(    
        name="Prepare data",    
        domino_job_config=DominoJobConfig(
            Command="python /mnt/scripts/prep-data.py",
        ),
        inputs={
            "data_path": str
        },
        outputs={
            # NOTE: Flyte normally suppports this -- but notice there are no partitions, which make them useless to Domino
            # this output is consumed by a subsequent task but also marked as an artifact
            "processed_data": Annotated[FlyteFile, Artifact(name="processed.sas7bdat")],
            # no downstream consumers -- simply an artifact output from an intermediate node in the graph
            "processed_data2": Annotated[FlyteFile, Artifact(name="processed2.sas7bdat")],
        },
        use_latest=True,
    )(data_path=data_path)

    training_results = DominoJobTask(
        name="Train model",
        domino_job_config=DominoJobConfig(            
            Command="python /mnt/scripts/train-model.py",
        ),
        inputs={
            "processed_data_in": FlyteFile,
            "epochs": int,
            "batch_size": int,
        },
        outputs={
            "model": FlyteFile,
        },
        use_latest=True,
    )(processed_data_in=data_prep_results.processed_data,epochs=10,batch_size=32)

    # return the result from 2nd node to the workflow annotated in different ways
    model = training_results['model']
    return model, model, model, model
