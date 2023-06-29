import sys
import pandas as pd

filepath = sys.argv[1]
txt_path = f'./Logs/{filepath}.txt'
csv_path = f'./Csvs/{filepath}.csv'

dataframe = pd.read_csv(txt_path)
dataframe.to_csv(csv_path, index = None)
