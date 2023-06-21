import pandas as pd

dataframe = pd.read_csv('./Logs/target_100000_141_packages_withgithub.txt')
dataframe.to_csv('./Csvs/target_100000_141_packages_withgithub.csv', index = None)
