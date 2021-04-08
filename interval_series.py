import math
import os
import numpy as np
import pandas as pd
from itertools import accumulate, product
from tabulate import tabulate


def display(df):
    print(' ')
    print(tabulate(df, headers='keys', tablefmt='github'))
    
# ввести все значения слева и интервал  
n = int(input('Wpisz rozmiar tablicy: '))
Xi_lp = list(map(int, input(
    'Wpisz wartosci cechy (xi) oddzielone spacja: ').strip().split()))[:n]
Xi_rp = list(map(int, input(
    'Wpisz wartosci cechy (xi) oddzielone spacja: ').strip().split()))[:n]
Fi = list(map(int, input(
    'Wpisz liczebnosci (fi) z jakimi te wartosci wystepuja: ').strip().split()))[:n]

Xi_lp = [20, 25, 30, 35, 40]
Xi_rp = [25, 30, 35, 40, 45]

Xi_avg = [(i + j) / 2 for i, j in zip(Xi_lp, Xi_rp)]
print(Xi_avg)

Fi = [14, 16, 23, 24, 10]

df_interval = pd.DataFrame({'Fi': Fi, 'Xi_avg': Xi_avg}, index = pd.IntervalIndex.from_arrays(Xi_lp, Xi_rp))
df_interval.index.name ='Xi'
display(df_interval) 
os.system("pause")