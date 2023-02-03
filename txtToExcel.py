import pandas as pd

dataframe = pd.read_csv('top_491_with_deps_5_90.txt')
dataframe.to_csv('top_491_with_deps_5_90.csv', index = None)
