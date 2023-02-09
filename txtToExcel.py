import pandas as pd

dataframe = pd.read_csv('top_dependencies_updated.txt')
dataframe.to_csv('top_dependencies_updated.csv', index = None)
