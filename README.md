# Domino AI Training Flow

This repo mocks a sample AI training script using Domino Flows. 

The input to this flow is the path to a sample dataset that is provided in this repository.

To run the flow, execute the following command in a workspace: 

```
pyflyte run --remote workflow.py training_workflow --data_path /mnt/code/data/data.csv
```

If you want to change the input data, replace the `data_path` parameter with the location to your input data. This can point to a location in your dataset snapshots.

# Flow Definition

The sample flow contains two tasks - one for data preparation and one for model training. This section explains each of the steps in detail:

** Data preparation **

The code snippet below shows the definition for the data preparation task

```
data_prep_results = run_domino_job(
    name="Prepare data",
    environment="Data Prep Environment",
    hardware_tier="Small",
    command="python /mnt/code/scripts/prep-data.py",
    inputs=[
        Input(name="data_path", type=str, value=data_path)
    ],
    outputs=[
        Output(name="processed_data", type=FlyteFile)
    ]
)
```


# Flow Scripts