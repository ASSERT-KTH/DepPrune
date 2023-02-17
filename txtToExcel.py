import pandas as pd

dataframe = pd.read_csv('collection_transitive_level.txt')
dataframe.to_csv('collection_transitive_level.csv', index = None)
