import math
import os
import numpy as np
from numpy.lib import median
import pandas as pd
from itertools import accumulate, product
from tabulate import tabulate


def display(df):
    print(' ')
    print(tabulate(df, headers='keys', tablefmt='github'))
    
# !!! input all 'left' values and find interval 

# n = int(input('Wpisz rozmiar tablicy: '))
# Xi_lp = list(map(int, input(
#     'Wpisz wartosci cechy (xi) oddzielone spacja: ').strip().split()))[:n]
# Xi_rp = list(map(int, input(
#     'Wpisz wartosci cechy (xi) oddzielone spacja: ').strip().split()))[:n]
# Fi = list(map(int, input(
#     'Wpisz liczebnosci (fi) z jakimi te wartosci wystepuja: ').strip().split()))[:n]

Xi_lp = [20, 25, 30, 35, 40]
Xi_rp = [25, 30, 35, 40, 45]
Xi_length_range = Xi_rp[0] - Xi_lp[0]

# Xi_avg -----------------------------------------------------
Xi_avg = [(i + j) / 2 for i, j in zip(Xi_lp, Xi_rp)]
Fi = [14, 16, 23, 24, 10]
# creating interval dict
interval_dict = {'Fi': Fi, 'Xi\'': Xi_avg}
# FiXi_avg ---------------------------------------------------
FiXi_avg = [i * j for i, j in zip(Xi_avg, Fi)]
# FiKu -------------------------------------------------------
FiKu = list(accumulate(Fi))
# Xi2_avg ----------------------------------------------------
Xi2_avg = [i**2 for i in Xi_avg]
# FiXi2_avg --------------------------------------------------
FiXi2_avg = [i * j for i, j in zip(Xi2_avg, Fi)]

interval_dict.update({'Fi * Xi\'': FiXi_avg, 'Fi Kum': FiKu, 'Xi^2\'': Xi2_avg, 'Fi * Xi^2\'': FiXi2_avg})

# Creating a dataframe, making intervals
index_interval = pd.IntervalIndex.from_arrays(Xi_lp, Xi_rp)
df_interval = pd.DataFrame(data=interval_dict, index = index_interval)
df_interval.index.name ='Xi'

# lower limit of the modal range
# ! function ???
max_Fi_value = max(Fi)
max_Fi_index = Fi.index(max_Fi_value)

prev_max_Fi_index = max_Fi_index - 1
prev_max_Fi_value = Fi[prev_max_Fi_index]

next_max_Fi_index = max_Fi_index + 1
next_max_Fi_value = Fi[next_max_Fi_index]

Xm = Xi_lp[max_Fi_index]

# Descriptive measures ********łł*********************************************************************
# Mean ------------------------------------------
avarage = round(df_interval.loc[:, 'Fi * Xi\''].sum() / sum(Fi), 2)
print('avg: ', avarage)
# Mode ------------------------------------------
mode = round(Xm + ((max_Fi_value - prev_max_Fi_value) / ((max_Fi_value - prev_max_Fi_value) + (max_Fi_value - next_max_Fi_value))) * Xi_length_range, 2)
print('mode: ', mode)
# Median ----------------------------------------
n_div_2 = sum(Fi) / 2
for i in FiKu:
    if n_div_2 < i:
        Xs_value = i
        break

Xs_index = FiKu.index(Xs_value)
Xs = Xi_lp[Xs_index]
# median = Xs + ((()) / Fi[])

print(n_div_2)
print(Xs)


# median = round(df_cumulative_series.loc[:, 'Xi'].median(), 2)



display(df_interval) 
os.system("pause")