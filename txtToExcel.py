import pandas as pd

dataframe = pd.read_csv('top_dependencies_5_92.txt')
dataframe.to_csv('top_dependencies_5_92.csv', index = None)
