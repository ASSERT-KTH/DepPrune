import pandas as pd

dataframe = pd.read_csv('top43_url.txt')
dataframe.to_csv('top43_url.csv', index = None)