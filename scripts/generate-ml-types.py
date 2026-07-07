import os
import shutil
from pathlib import Path

OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "/workflow/outputs")
SHOULD_APPEND_FILE_EXT = os.environ.get("SHOULD_APPEND_FILE_EXT", "").lower() in ("1", "true", "yes")
ARTIFACTS_DIR = "/mnt/code/artifacts"

if not Path(OUTPUT_DIR).exists():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

outputs = [
    ("csv",          "data.csv"),
    ("json",         "test.json"),
    ("png",          "plot.png"),
    ("jpeg",         "plot.jpeg"),
    ("notebook",     "notebook.ipynb"),
    ("pkl",          "intro.pkl"),
    ("mlflow_model", "model"),
]

for named_output, filename in outputs:
    source = Path(ARTIFACTS_DIR) / filename
    dest_name = filename if SHOULD_APPEND_FILE_EXT else named_output
    dest = Path(OUTPUT_DIR) / dest_name
    try:
        if source.is_dir():
            shutil.copytree(source, dest)
        else:
            shutil.copy(source, dest)
        print(f"Created {named_output} output")
    except Exception as e:
        print(f"Error: {e}")
        raise SystemExit(1)