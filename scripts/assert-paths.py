import os
import pandas as pd
from time import sleep

# Read input data. Inputs are stored in a blob at /workflow/inputs/<NAME OF INPUT>.
data_path_df = "/workflow/inputs/{}.csv".format("processed_data_domino_file") # DominoFile
data_path_ff = "/workflow/inputs/{}".format("processed_data_flyte_file") # FlyteFile
data_path_dfl = "/workflow/inputs/{}".format("processed_data_domino_file_legacy") # DominoFileLegacy
data_path_dflcsv = "/workflow/inputs/{}.csv".format("processed_data_domino_file_legacy") # DominoFileLegacy
df = pd.read_csv(data_path_df)
ff = pd.read_csv(data_path_ff)
dfl = pd.read_csv(data_path_dfl)
dflcsv = pd.read_csv(data_path_dflcsv)

assert len(df) > 0
assert len(ff) > 0
assert len(dfl) > 0
assert len(dflcsv) > 0

# Pretend like something is happening here to train the model
print("Training the model")
sleep(20)

# Write output. Outputs must be written to /workflow/outputs/<NAME OF OUTPUT> for it to be tracked.
named_output = "model"
os.mkdir("/workflow/outputs/{}".format(named_output)) 
