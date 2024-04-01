import os
import pandas as pd
from time import sleep

# Read input data
named_input = "processed_data"
data_path = "/workflow/inputs/{}".format(named_input)
df = pd.read_csv(data_path)

# Pretend like something is happening here to train the model
sleep(20)

# Write output
named_output = "model"
os.mkdir("/workflow/outputs/{}".format(named_output)) 

# Write output success
with open("/workflow/outputs/_SUCCESS", "w+"):
    pass
