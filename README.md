# Domino AI Training Flow

This repo mocks a sample AI training script using Domino Flows. 

The input to this flow is the path to a sample dataset that is provided in this repository.

To run the flow, execute the following command in a workspace: 

```
pyflyte run --remote workflow.py training_workflow --data_path /mnt/code/data/data.csv
```

If you want to change the input data, replace the `data_path` parameter with the location to your input data. This can point to a location in your dataset snapshots.

# Flow Definition

# Flow Scripts