import pandas as pd

dataframe = pd.read_csv('./Logs/repo_CommonJS_100000.txt')
dataframe.to_csv('./Csvs/repo_CommonJS_100000.csv', index = None)
