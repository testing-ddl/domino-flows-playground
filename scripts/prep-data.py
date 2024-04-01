import pandas as pd
import argparse

# Read input data
named_input = "data_path"
data_path = "/workflow/inputs/{}".format(named_input)
df = pd.read_csv(data_path)

# Process data
print(df)
df = df.drop('a', axis=1)
print(df)

# Write output
named_output = "processed_data"
df.to_csv("/workflow/outputs/{}".format(named_output))

# Write output success
with open("/workflow/outputs/_SUCCESS", "w+"):
    pass
