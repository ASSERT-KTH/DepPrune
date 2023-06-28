import pandas as pd

dataframe = pd.read_csv('./Logs/temp_test_intersection.txt')
dataframe.to_csv('./Csvs/temp_test_intersection.csv', index = None)
