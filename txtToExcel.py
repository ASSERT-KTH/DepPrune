import pandas as pd

dataframe = pd.read_csv('top3000_url_duplicated.txt')
dataframe.to_csv('top3000_url_duplicated.csv', index = None)