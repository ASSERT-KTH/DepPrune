import pandas as pd

dataframe = pd.read_csv('collection_bloated_level.txt')
dataframe.to_csv('collection_bloated_level.csv', index = None)
