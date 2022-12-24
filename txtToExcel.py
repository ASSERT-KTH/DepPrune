import pandas as pd

dataframe = pd.read_csv('top100install.txt')
dataframe.to_csv('top100install.csv', index = None)