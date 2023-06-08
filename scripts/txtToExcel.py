import pandas as pd

dataframe = pd.read_csv('./Logs/repo_NodeJS_100000_commits.txt')
dataframe.to_csv('./Csvs/repo_NodeJS_100000_commits.csv', index = None)
