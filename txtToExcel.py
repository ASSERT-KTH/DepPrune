import pandas as pd

dataframe = pd.read_csv('top_dependencies_temp.txt')
dataframe.to_csv('top_dependencies_temp.csv', index = None)