from typing import Tuple, TypeVar
from flytekitplugins.domino.helpers import (
    Input,
    Output,
    run_domino_job_task,
)
from flytekitplugins.domino.artifact import (
    Artifact,
    DATA,
    MODEL,
    REPORT,
)
from flytekit import workflow
from flytekit.types.file import FlyteFile

TrainingDataReportArtifact = Artifact("Prepped Training Data Report", REPORT)
ModelAccuracyReportArtifact = Artifact("Model Accuracy Report", REPORT)

ModelArtifactOne = Artifact("Model One", MODEL)
ModelArtifactTwo = Artifact("Model Two", MODEL)
ModelArtifactThree = Artifact("Model Three", MODEL)

PredictionsArtifact = Artifact("Model Predictions", DATA)

# pyflyte run --remote complex.py complex_artifact_flow --training_data=input_data.csv --test_data=test_data.csv
@workflow
def complex_artifact_flow(training_data: FlyteFile[TypeVar("csv")], test_data: FlyteFile[TypeVar("csv")]) -> Tuple[
    TrainingDataReportArtifact.File(name="Summary Stats", type="txt"),
    TrainingDataReportArtifact.File(name="Data Vizualization", type="jpg"),
    ModelArtifactOne.File(name="Model One", type="pkl"),
    ModelArtifactTwo.File(name="Model Two", type="pkl"),
    ModelArtifactThree.File(name="some_propriatary_format.extensionfoobarbaz"),
    ModelArtifactThree.File(name="model_metadata_one.pkl"),
    ModelArtifactThree.File(name="model_metadata_two.pkl"),
    ModelArtifactThree.File(name="model_metadata_three.pkl"),
    PredictionsArtifact.File(name="model_one_predictions.csv"),
    PredictionsArtifact.File(name="model_two_predictions.csv"),
    PredictionsArtifact.File(name="model_three_predictions.csv"),
    ModelAccuracyReportArtifact.File(name="model_one_accuracy_report.pdf"),
    ModelAccuracyReportArtifact.File(name="model_two_accuracy_report.pdf"),
    ModelAccuracyReportArtifact.File(name="model_three_accuracy_report.pdf"),
]:
    """
    A complex flow demonstrating producing multiple artifacts with multiple files from multiple tasks.
    """
    input_stats, input_viz, prepped_training_data = run_domino_job_task(
        flyte_task_name="Prep data",
        command="prep_data.py",
        inputs=[
            Input(name="input_data", type=FlyteFile[TypeVar("csv")], value=training_data)
        ],
        output_specs=[
            Output(name="stats", type=FlyteFile[TypeVar("txt")]),
            Output(name="viz", type=FlyteFile[TypeVar("jpg")]),
            Output(name="prepped_data", type=FlyteFile[TypeVar("csv")]),
        ],
        use_project_defaults_for_omitted=True,
    )

    test_data, test_labels = run_domino_job_task(
        flyte_task_name="Mask Data",
        command="mask_data.py",
        inputs=[
            Input(name="input_data", type=FlyteFile[TypeVar("csv")], value=test_data),
        ],
        output_specs=[
            Output(name="data", type=FlyteFile[TypeVar("csv")]),
            Output(name="labels", type=FlyteFile[TypeVar("csv")]),
        ],
        use_project_defaults_for_omitted=True,
    )

    model_one = run_domino_job_task(
        flyte_task_name="Make Model One",
        command="make_model_one.py",
        inputs=[
            Input(name="training_data", type=FlyteFile[TypeVar("csv")], value=prepped_training_data)
        ],
        output_specs=[
            Output(name="model", type=FlyteFile[TypeVar("pkl")]),
        ],
        use_project_defaults_for_omitted=True,
    )
    model_one_predictions = run_domino_job_task(
        flyte_task_name="Classify Model One",
        command="classify_model_one.py",
        inputs=[
            Input(name="model", type=FlyteFile[TypeVar("pkl")], value=model_one),
            Input(name="data_points", type=FlyteFile[TypeVar("csv")], value=test_data)
        ],
        output_specs=[
            Output(name="predictions", type=FlyteFile[TypeVar("csv")]),
        ],
        use_project_defaults_for_omitted=True,
    )
    model_one_accuracy = run_domino_job_task(
        flyte_task_name="Accuracy Report Model One",
        command="make_accuracy_report.py",
        inputs=[
            Input(name="predictions", type=FlyteFile[TypeVar("csv")], value=model_one_predictions),
            Input(name="labels", type=FlyteFile[TypeVar("csv")], value=test_labels),
        ],
        output_specs=[
            Output(name="accuracy", type=FlyteFile[TypeVar("pdf")]),
        ],
        use_project_defaults_for_omitted=True,
    )

    model_two = run_domino_job_task(
        flyte_task_name="Make Model Two",
        command="make_model_two.py",
        inputs=[
            Input(name="training_data", type=FlyteFile[TypeVar("csv")], value=prepped_training_data)
        ],
        output_specs=[
            Output(name="model", type=FlyteFile[TypeVar("pkl")]),
        ],
        use_project_defaults_for_omitted=True,
    )
    model_two_predictions = run_domino_job_task(
        flyte_task_name="Classify Model Two",
        command="classify_model_two.py",
        inputs=[
            Input(name="model", type=FlyteFile[TypeVar("pkl")], value=model_two),
            Input(name="data_points", type=FlyteFile[TypeVar("csv")], value=test_data)
        ],
        output_specs=[
            Output(name="predictions", type=FlyteFile[TypeVar("csv")]),
        ],
        use_project_defaults_for_omitted=True,
    )
    model_two_accuracy = run_domino_job_task(
        flyte_task_name="Accuracy Report Model Two",
        command="make_accuracy_report.py",
        inputs=[
            Input(name="predictions", type=FlyteFile[TypeVar("csv")], value=model_two_predictions),
            Input(name="labels", type=FlyteFile[TypeVar("csv")], value=test_labels),
        ],
        output_specs=[
            Output(name="accuracy", type=FlyteFile[TypeVar("pdf")]),
        ],
        use_project_defaults_for_omitted=True,
    )

    model_three, model_three_meta_one, model_three_meta_two, model_three_meta_three = run_domino_job_task(
        flyte_task_name="Make Model Three",
        command="make_model_three.py",
        inputs=[
            Input(name="training_data", type=FlyteFile[TypeVar("csv")], value=prepped_training_data)
        ],
        output_specs=[
            Output(name="model", type=FlyteFile[TypeVar("extensionfoobarbaz")]),
            Output(name="model_meta_one", type=FlyteFile[TypeVar("pkl")]),
            Output(name="model_meta_two", type=FlyteFile[TypeVar("pkl")]),
            Output(name="model_meta_three", type=FlyteFile[TypeVar("pkl")]),
        ],
        use_project_defaults_for_omitted=True,
    )
    model_three_predictions = run_domino_job_task(
        flyte_task_name="Classify Model Three",
        command="classify_model_three.py",
        inputs=[
            Input(name="model", type=FlyteFile[TypeVar("extensionfoobarbaz")], value=model_three),
            Input(name="model_meta_one", type=FlyteFile[TypeVar("pkl")], value=model_three_meta_one),
            Input(name="model_meta_two", type=FlyteFile[TypeVar("pkl")], value=model_three_meta_two),
            Input(name="model_meta_three", type=FlyteFile[TypeVar("pkl")], value=model_three_meta_three),
            Input(name="data_points", type=FlyteFile[TypeVar("csv")], value=test_data)
        ],
        output_specs=[
            Output(name="predictions", type=FlyteFile[TypeVar("csv")]),
        ],
        use_project_defaults_for_omitted=True,
    )
    model_three_accuracy = run_domino_job_task(
        flyte_task_name="Accuracy Report Model Three",
        command="make_accuracy_report.py",
        inputs=[
            Input(name="predictions", type=FlyteFile[TypeVar("csv")], value=model_three_predictions),
            Input(name="labels", type=FlyteFile[TypeVar("csv")], value=test_labels),
        ],
        output_specs=[
            Output(name="accuracy", type=FlyteFile[TypeVar("pdf")]),
        ],
        use_project_defaults_for_omitted=True,
    )

    return (
        input_stats,
        input_viz,
        model_one,
        model_two,
        model_three,
        model_three_meta_one,
        model_three_meta_two,
        model_three_meta_three,
        model_one_predictions,
        model_two_predictions,
        model_three_predictions,
        model_one_accuracy,
        model_two_accuracy,
        model_three_accuracy,
    )