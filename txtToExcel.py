import pandas as pd

dataframe = pd.read_csv('top_dependencies_greater5_test.txt')
dataframe.to_csv('top_dependencies_greater5_test.csv', index = None)