import pandas as pd

dataframe = pd.read_csv('./Logs/repo_100000_readme.txt')
dataframe.to_csv('./Csvs/repo_100000_readme.csv', index = None)
