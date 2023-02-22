import pandas as pd

dataframe = pd.read_csv('top_target_174_unused_bloated.txt')
dataframe.to_csv('top_target_174_unused_bloated.csv', index = None)
