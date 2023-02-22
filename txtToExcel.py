import pandas as pd

dataframe = pd.read_csv('top_target_174_unused_bloated_in_deps.txt')
dataframe.to_csv('top_target_174_unused_bloated_in_deps.csv', index = None)
