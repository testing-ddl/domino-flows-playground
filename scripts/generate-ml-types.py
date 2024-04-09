import shutil

# CSV File
named_output = "csv"
source = "/mnt/code/artifacts/data.csv"
dest = f"/workflow/outputs/{named_output}"
shutil.copy(source, dest)
print("Created CSV output")

# MLFlow Mode
named_output = "mlflow_model"
source = "/mnt/code/artifacts/model"
dest = f"/workflow/outputs/{named_output}"
shutil.copytree(source, dest)
print("Created MLflow model output")

