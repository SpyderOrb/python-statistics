import math
import os
import numpy as np
from numpy.lib import median
import pandas as pd
from itertools import accumulate, product
from tabulate import tabulate

# Współczynnik korelacji (korelogram)
# Liniowa funkcja regresji

# n = int(input('Wpisz rozmiar tablicy: '))
# Xi = list(map(int, input('Wpisz wartosc cechy Xi oddzielone spacja: ').strip().split()))[:n]
# Yi = list(map(int, input('Wpisz wartosc cechy Yi oddzielone spacja: ').strip().split()))[:n]
Xi = [16, 25, 24, 50, 60]
Yi = [95, 163, 250, 297, 335]

df_correlation = pd.DataFrame(list(zip(Xi, Yi)), columns=['Xi', 'Yi'])
# Xi, Yi averages
Xi_avg = df_correlation.loc[:, 'Xi'].mean()
Yi_avg = df_correlation.loc[:, 'Yi'].mean()
# Xi - Xi_avg, Yi - Yi_avg
Xi_diff_Xi_avg = [(i - Xi_avg) for i in Xi]
Yi_diff_Yi_avg = [(i - Yi_avg) for i in Yi]
df_correlation['Xi-Xi_avg'] = Xi_diff_Xi_avg
df_correlation['Yi-Yi_avg'] = Yi_diff_Yi_avg
# (Xi - Xi_avg)^2, (Yi - Yi_avg)^2
Xi_diff_Xi_avg2 = [i**2 for i in Xi_diff_Xi_avg]
Yi_diff_Yi_avg2 = [i**2 for i in Yi_diff_Yi_avg]
df_correlation['Xi-Xi_avg ^2'] = Xi_diff_Xi_avg2
df_correlation['Yi-Yi_avg ^2'] = Yi_diff_Yi_avg2
# df_correlation['Xi-Xi_avg'] = Xi_diff_Xi_avg
# Xi_diff_Xi_avg = []
# Yi_diff_Yi_avg = []

# for column in df_correlation[['Xi']]:#     columnSeriesObj = df_correlation[column]
#     Xi_diff_Xi_avg.append(columnSeriesObj - Xi_avg)

# for column in df_correlation[['Yi']]:
#     columnSeriesObj = df_correlation[column]
#     Yi_diff_Yi_avg.append(columnSeriesObj - Yi_avg)

col_Xi = df_correlation['Xi'].tolist()
col_Yi = df_correlation['Yi'].tolist()

# df_correlation = df_correlation.append({'Xi - Xi_avg':Xi_diff_Xi_avg})
# df_Xi_diff_Xi_avg = pd.DataFrame(Xi_diff_Xi_avg)
# df_correlation['Xi - Xi_avg'] = Xi_diff_Xi_avg
print(col_Xi)
print(col_Yi)
print(df_correlation, '\n')
print(Xi_avg, '\n')
print(Yi_avg)
