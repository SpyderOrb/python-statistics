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

def quartiles(div_of_N):
    n_div = sum(Fi) * div_of_N

    for i in FiKu:
        if n_div < i:
            Xs_value = i
            break

    Xs_index = FiKu_index = FiKu.index(Xs_value)
    Xs = Xi_lp[Xs_index]
    sum_preceding_Fiku_index = FiKu_index - 1
    sum_preceding_Fiku = FiKu[sum_preceding_Fiku_index]
    result = round(Xs + (((n_div - sum_preceding_Fiku) * Xi_length_range) / Fi[Xs_index]), 2)
    return result
    
n = int(input('Wpisz rozmiar tablicy: '))
Xi_lp = list(map(int, input(
    'Wpisz wartosci cechy (xdj) z (xdj; xgj] oddzielone spacja: ').strip().split()))[:n]
Xi_length_range = int(input('Wpisz dlugosc przedzilu: '))
Xi_rp = [i + Xi_length_range for i in Xi_lp]
Fi = list(map(int, input(
    'Wpisz liczebnosci (fi) z jakimi te wartosci wystepuja: ').strip().split()))[:n]

# Xi_avg -----------------------------------------------------
Xi_avg = [(i + j) / 2 for i, j in zip(Xi_lp, Xi_rp)]
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

interval_dict.update(
    {'Fi * Xi\'': FiXi_avg, 'Fi Kum': FiKu,
    'Xi^2\'': Xi2_avg, 'Fi * Xi^2\'': FiXi2_avg}
)

# Creating a dataframe, making intervals
index_interval = pd.IntervalIndex.from_arrays(Xi_lp, Xi_rp)
df_interval = pd.DataFrame(data=interval_dict, index = index_interval)
df_interval.index.name ='Xi'

# lower limit of the modal range
# ! function ???
max_Fi_value = max(Fi) 
max_Fi_index = Fi.index(max_Fi_value) 

prev_max_Fi_index = max_Fi_index - 1 
try:
    prev_max_Fi_value = Fi[prev_max_Fi_index]
except IndexError:
    prev_max_Fi_value = 0

next_max_Fi_index = max_Fi_index + 1
try:
    next_max_Fi_value = Fi[next_max_Fi_index]
except IndexError:
    next_max_Fi_value = 0
Xm = Xi_lp[max_Fi_index]

# Descriptive measures ********************************************************************************
# Mean ------------------------------------------
avarage = round(df_interval.loc[:, 'Fi * Xi\''].sum() / sum(Fi), 2)
print('avg:', avarage)
# Mode ------------------------------------------
mode = round(Xm + ((max_Fi_value - prev_max_Fi_value) / ((max_Fi_value - prev_max_Fi_value) \
    + (max_Fi_value - next_max_Fi_value))) * Xi_length_range, 2)
print('mode:', mode)
# Median -----------------------------------------
median = quartiles(0.5)
print('func median:', median)
# Lower quartile ---------------------------------
Q1 = quartiles(0.25)
print('func Lower quartile:', Q1)
# Upper quartile ---------------------------------
Q3 = quartiles(0.75)
print('func Upper quartile:', Q3)
# Variance ---------------------------------------
variance = round((1 / df_interval.loc[:, 'Fi'].sum()) * df_interval.loc[:, 'Fi * Xi^2\''].sum() \
    - pow((avarage), 2), 4)
print('Wariancja:',variance)
# std --------------------------------------------
std = round(math.sqrt(variance), 2)
print('std:', std)
# cv ---------------------------------------------
cv = round(std / abs(avarage) * 100, 2)
print('cv:',cv)
# asymmetry --------------------------------------
# ! if '-' - lewostronna, '+' - prawostronna, (silna, umierkowana, slaba)
asymmetry = round(((avarage - mode) / std), 4)
print('asymmetry:', asymmetry)

df_interval_row_sum = pd.DataFrame(
    {'Fi': sum(Fi), 'Fi * Xi\'': sum(FiXi_avg), 'Fi * Xi^2\'': sum(FiXi2_avg)}, 
    index=['sum']
).astype(np.float64)

df_interval_descriptive_measures = pd.DataFrame(
    {'srednia': avarage, 'Me': median,
    'Mo': mode, 'Kwartyl dolny': Q1,
    'Kwartyl gorny': Q3, 'wariancja': variance,
    'od standardowe': std, 'wsp zmiennosci': cv,
    'asymetria': asymmetry},
    index=['measures']
).astype(np.float64)

display(df_interval) 
display(df_interval_row_sum)
display(df_interval_descriptive_measures)
os.system("pause") 