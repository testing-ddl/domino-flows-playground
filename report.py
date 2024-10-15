import pandas
import shutil

# convert csv to HTML
df = pandas.read_csv('/workflow/inputs/data', sep=',') 
df.to_html('/workflow/outputs/html') 

# dummy graph
shutil.copyfile('pie-chart.png', '/workflow/outputs/graph')