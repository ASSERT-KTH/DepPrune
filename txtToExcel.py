import pandas as pd

dataframe = pd.read_csv('top_dependencies_greater1_test_random.txt')
dataframe.to_csv('top_dependencies_greater1_test_random.csv', index = None)