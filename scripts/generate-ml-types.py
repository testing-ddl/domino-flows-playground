import shutil
import os

os.makedirs("/mnt/data/flow-outputs", exist_ok=True)

# CSV File
source = "/mnt/code/artifacts/data.csv"
dest = f"/mnt/data/flow-outputs/data.csv"
try:
    shutil.copy(source, dest)
    print("Created CSV output")
except Exception as e:
    print(f"Error: {e}")

# CSV File
source = "/mnt/code/artifacts/test.json"
dest = f"/mnt/data/flow-outputs/test.json"
try:
    shutil.copy(source, dest)
    print("Created JSON output")
except Exception as e:
    print(f"Error: {e}")

# PNG File
source = "/mnt/code/artifacts/plot.png"
dest = f"/mnt/data/flow-outputs/plot.png"
try:
    shutil.copy(source, dest)
    print("Created PNG output")
except Exception as e:
    print(f"Error: {e}")

# JPEG File
source = "/mnt/code/artifacts/plot.jpeg"
dest = f"/mnt/data/flow-outputs/plot.jpeg"
try:
    shutil.copy(source, dest)
    print("Created JPEG output")
except Exception as e:
    print(f"Error: {e}")

# Notebook File
source = "/mnt/code/artifacts/notebook.ipynb"
dest = f"/mnt/data/flow-outputs/notebook.ipynb"
try:
    shutil.copy(source, dest)
    print("Created Notebook output")
except Exception as e:
    print(f"Error: {e}")

# Pkl File
source = "/mnt/code/artifacts/intro.pkl"
dest = f"/mnt/data/flow-outputs/intro.pkl"
try:
    shutil.copy(source, dest)
    print("Created Pkl output")
except Exception as e:
    print(f"Error: {e}")

# MLFlow Model
named_output = "mlflow_model"
source = "/mnt/code/artifacts/model"
dest = f"/workflow/outputs/{named_output}"
try:
    shutil.copytree(source, dest)
    print("Created MLflow model output")
except Exception as e:
    print(f"Error: {e}")
