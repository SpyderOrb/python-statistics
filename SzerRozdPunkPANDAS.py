print('''

   _____ __        __             __        __                        _                         
  / ___// /_____ _/ /___  _______/ /___  __/ /______ _   ____  ____  (_)________ _      ______ _
  \__ \/ __/ __ `/ __/ / / / ___/ __/ / / / //_/ __ `/  / __ \/ __ \/ / ___/ __ \ | /| / / __ `/
 ___/ / /_/ /_/ / /_/ /_/ (__  ) /_/ /_/ / ,< / /_/ /  / /_/ / /_/ / (__  ) /_/ / |/ |/ / /_/ / 
/____/\__/\__,_/\__/\__, /____/\__/\__, /_/|_|\__,_/   \____/ .___/_/____/\____/|__/|__/\__,_/  
                   /____/         /____/                   /_/                                  

''')

import numpy as np
import pandas as pd
import math
from itertools import accumulate
from tabulate import tabulate


def display(df):
    print(' ')
    print(tabulate(df, headers='keys', tablefmt='github'))
    

n = int(input('Wpisz rozmiar tablicy: '))
Xi = list(map(int, input(
    'Wpisz wartosci cechy (xi) oddzielone spacja: ').strip().split()))[:n]
Fi = list(map(int, input(
    'Wpisz liczebnosci (fi) z jakimi te wartosci wystepuja: ').strip().split()))[:n]
# Xi, Fi ---------------------------------------------------
main_dict = {'Xi': Xi, 'Fi': Fi}
# FiXi -----------------------------------------------------
FiXi = [i * j for i, j in zip(Xi, Fi)]
main_dict.update({'FiXi': FiXi})
# Xi2 ------------------------------------------------------
Xi2 = [i**2 for i in Xi]
main_dict.update({'Xi2': Xi2})
# FiXi2 ----------------------------------------------------
FiXi2 = [i * j for i, j in zip(Xi2, Fi)]
main_dict.update({'FiXi2': FiXi2})
# FiKu -----------------------------------------------------
FiKu = list(accumulate(Fi))
main_dict.update({'FiKu': FiKu})

# Comulative series ----------------------------------------
cumulative_series = []
for i, j in zip(Xi, Fi):
    count = 0
    while j != count:
        cumulative_series.append(i)
        count += 1
cumulative_series_dict = {'Xi': cumulative_series}
df_cumulative_series = pd.DataFrame(data=cumulative_series_dict, dtype=np.int64)

# Сreating a dataframe
df_main = pd.DataFrame(data=main_dict, dtype=np.int64)

# Descriptive measures *****************************************************************************
# Mean ------------------------------------------
avarage = round(df_main.loc[:, 'FiXi'].sum() / sum(Fi), 2)
# Median ----------------------------------------
median = round(df_cumulative_series.loc[:, 'Xi'].median(), 2)
# Mode ------------------------------------------
mode = df_cumulative_series.loc[:, 'Xi'].mode().values[0]
# Variance --------------------------------------
variance = round((1 / df_main.loc[:, 'Fi'].sum()) * df_main.loc[:, 'FiXi2'].sum() - pow((avarage), 2), 2)
# std -------------------------------------------
std = round(math.sqrt(variance), 2)
# cv --------------------------------------------
cv = round(std / abs(avarage) * 100, 2)

df_row_sum = pd.DataFrame(
    {'Fi': sum(Fi), 'FiXi': sum(FiXi), 'FiXi2': sum(FiXi2)}, 
    index=['sum']
).fillna(0).astype(int)

df_descriptive_measures = pd.DataFrame(
    {'srednia': avarage, 'Me': median,
    'Mo': mode, 'wariancja': variance,
    'od standardowe': std, 'wsp zmiennosci': cv },
    index=['measures']
).astype(float)

display(df_main)
display(df_row_sum)
display(df_descriptive_measures)