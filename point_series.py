import math
import os
import numpy as np
import pandas as pd
from itertools import accumulate
from tabulate import tabulate
import time
from datetime import timedelta

start_time = time.monotonic()

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
# Xi2 ------------------------------------------------------
Xi2 = [i**2 for i in Xi]
# FiXi2 ----------------------------------------------------
FiXi2 = [i * j for i, j in zip(Xi2, Fi)]
# FiKu -----------------------------------------------------
FiKu = list(accumulate(Fi))

main_dict.update(
    {'Fi * Xi': FiXi, 'Xi^2': Xi2,
    'Fi * Xi^2': FiXi2, 'Fi Kum': FiKu}
)

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
df_main.index.name = 'id'

# Descriptive measures *****************************************************************************
# Mean ------------------------------------------
avarage = round(df_main.loc[:, 'Fi * Xi'].sum() / sum(Fi), 2)
# Median ----------------------------------------
median = round(df_cumulative_series.loc[:, 'Xi'].median(), 2)
# Mode ------------------------------------------
mode = df_cumulative_series.loc[:, 'Xi'].mode().values[0]
# Variance --------------------------------------
variance = round((1 / df_main.loc[:, 'Fi'].sum()) * df_main.loc[:, 'Fi * Xi^2'].sum() - pow((avarage), 2), 4)
# std -------------------------------------------
std = round(math.sqrt(variance), 2)
# cv --------------------------------------------
cv = round(std / abs(avarage) * 100, 2)

df_row_sum = pd.DataFrame(
    {'Fi': sum(Fi), 'Fi * Xi': sum(FiXi), 'Fi * Xi2': sum(FiXi2)}, 
    index=['sum']
).astype(np.float64)

df_descriptive_measures = pd.DataFrame(
    {'srednia': avarage, 'Me': median,
    'Mo': mode, 'wariancja': variance,
    'od standardowe': std, 'wsp zmiennosci': cv },
    index=['measures']
).astype(np.float64)

display(df_main)
display(df_row_sum)
display(df_descriptive_measures)

end_time =  time.monotonic()
print('Duration: {}'.format(timedelta(seconds=end_time - start_time)))

os.system("pause")
