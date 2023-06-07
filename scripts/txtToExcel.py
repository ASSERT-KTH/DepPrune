import pandas as pd

dataframe = pd.read_csv('./Logs/repo_module_system_100000.txt')
dataframe.to_csv('./Logs/repo_module_system_100000.csv', index = None)
