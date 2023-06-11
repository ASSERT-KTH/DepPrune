import pandas as pd

dataframe = pd.read_csv('./Logs/repo_100000_readme_github.txt')
dataframe.to_csv('./Csvs/repo_100000_readme_github.csv', index = None)
