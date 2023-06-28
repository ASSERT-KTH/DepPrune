import pandas as pd

dataframe = pd.read_csv('./Logs/rerun_test_1000_commits_done.txt')
dataframe.to_csv('./Csvs/rerun_test_1000_commits_done.csv', index = None)
