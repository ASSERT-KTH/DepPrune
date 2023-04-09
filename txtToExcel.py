import pandas as pd

dataframe = pd.read_csv('collection_bloated_level_with_leaf.txt')
dataframe.to_csv('collection_bloated_level_with_leaf.csv', index = None)
