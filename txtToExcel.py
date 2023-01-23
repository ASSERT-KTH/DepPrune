import pandas as pd

dataframe = pd.read_csv('top_dependencies_greater1_test.txt')
dataframe.to_csv('top_dependencies_greater1_test.csv', index = None)