import pandas as pd

dataframe = pd.read_csv('top_total_file_number.txt')
dataframe.to_csv('top_total_file_number.csv', index = None)
