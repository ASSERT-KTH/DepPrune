import pandas as pd

dataframe = pd.read_csv('./Logs/repo_100000_potential_runnable.txt')
dataframe.to_csv('./Csvs/repo_100000_potential_runnable.csv', index = None)
