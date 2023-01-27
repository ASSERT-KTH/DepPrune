import pandas as pd

dataframe = pd.read_csv('top_target30.txt')
dataframe.to_csv('top_target30.csv', index = None)
