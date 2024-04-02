# Domino AI Training Flow

This repo mocks a sample AI training script using Domino Flows. 

The input to this flow is the path to a sample dataset that is provided in this repository.

To run the flow, execute the following command in a workspace: 

```
pyflyte run --remote workflow.py training_workflow --data_path /mnt/code/data/data.csv
```

Once the command is executed, a link to monitor the run will be displayed in the terminal.

If you want to change the input data, replace the `data_path` parameter with the location to your input data. This can point to a location in your dataset snapshots.

# Flow Definition

The flow is defined in the `workflow.py` file and it leverages some helper methods that are located in `utils/flyte.py`. It is reccommended that you do not modify the contents within the helper methods, but they are there for you if you want the full flexibility.

The sample flow contains two tasks - one for data preparation and one for model training. Each task ultimately triggers a Domino Job and returns the outputs. We'll go through each of the steps in detail.

**Data preparation**

The code snippet below shows the definition for the data preparation task:

```
data_prep_results = run_domino_job(
    name="Prepare data",
    command="python /mnt/code/scripts/prep-data.py",
    environment="Data Prep Environment",
    hardware_tier="Small",
    inputs=[
        Input(name="data_path", type=str, value=data_path)
    ],
    outputs=[
        Output(name="processed_data", type=FlyteFile)
    ]
)
```

As you can use the `run_domino_job` function to create the task with the appropriate parameters. Explaining each parameter in detail:

- `name`: The name for the task.
- `command`: The command that will be used in the Domino Job.
- `environment`: The name of the environment you want to use for the task. If not specified, the default environment for the project will be used.
- `hardware_tier`: The name of the hardware tier you want to use for the task. If not specified, the default hardware tier for the project will be used.
- `inputs`: A list of inputs that the task depends on. Note how the `data_path` input is set to the argument provided through the command line when starting the flow.
- `outputs`: A list of outputs that will be produced by that task. Supported input and output types are documented [here](https://docs.flyte.org/en/latest/user_guide/data_types_and_io/index.html)

Inputs can be accessed within Domino Jobs at `/workflow/inputs/<NAME OF INPUT>`. In a similar fashion, outputs must be written to `/workflow/outputs/<NAME OF OUTPUT>` inside the Domino Job for them to be tracked and returned in the task. See the scripts inside the `script` folder for more details.

**Model training**

The code snippet below shows the definition for the model training task:

```
training_results = run_domino_job(
    name="Train model",
    command="python /mnt/code/scripts/train-model.py",
    environment="Training Environment",
    hardware_tier="Medium",
    inputs=[
        Input(name="processed_data", type=FlyteFile, value=data_prep_results['processed_data']),
        Input(name="epochs", type=int, value=10),
        Input(name="batch_size", type=int, value=32)
    ],
    outputs=[
        Output(name="model", type=FlyteFile)
    ]
)
```

As you can see, the same `run_domino_job` function is used. A few things to note about the snippet above:
- Different command, environments, and hardware tiers can be used. It doesn't need to be the same as the other steps.
- The output from the data prep tasks is referenced via `data_prep_results['processed_data']` and it specified as an input to the training task.
