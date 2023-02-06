import pandas as pd

dataframe = pd.read_csv('top_coverage_80_100_info.txt')
dataframe.to_csv('top_coverage_80_100_info.csv', index = None)
