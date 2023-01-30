# %matplotlib inline
import pandas as pd
import ptitprince as pt

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

df = pd.read_csv('https://vincentarelbundock.github.io/Rdatasets/csv/datasets/iris.csv')

ax = pt.RainCloud(x = 'Species', y = 'Sepal.Length', 
                  data = df, 
                  width_viol = .8,
                  width_box = .4,
                  figsize = (12, 8), orient = 'h',
                  move = .0)
