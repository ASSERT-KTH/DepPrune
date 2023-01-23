import pandas as pd

dataframe = pd.read_csv('top_dependencies_greater1.txt')
dataframe.to_csv('top_dependencies_greater1.csv', index = None)