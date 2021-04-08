import numpy as np
import pandas as pd
from itertools import accumulate
from math import sqrt

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
# print('Szereg szczegolowy:', Detailed_series)
cumulative_series_dict = {'Xi': cumulative_series}
df_cumulative_series = pd.DataFrame(data=cumulative_series_dict, dtype=np.int64)
print('Do you want to print comulative series? ')
# print(pd_Detailed_series)

# Сreating a dataframe
df_main = pd.DataFrame(data=main_dict, dtype=np.int64)

# Descriptive measures *****************************************************************************

# Mean ------------------------------------------
avarage = df_main.loc[:, 'FiXi'].sum() / sum(Fi)
print('Srednia arytmetyczna:', avarage)

# Median ----------------------------------------
median = df_cumulative_series.loc[:, 'Xi'].median()
print('Mediana:', median)

# Mode ------------------------------------------
# mode = pd_Detailed_series['Xi'].mode()
# mode.index = ['Mo: ']
mode = df_cumulative_series.loc[:, 'Xi'].mode().values[0]
print('Modalna:', mode)

# Variance --------------------------------------
variance = (1 / df_main.loc[:, 'Fi'].sum()) * df_main.loc[:, 'FiXi2'].sum() - pow((avarage), 2)
print('Wariancja:', variance)

# std -------------------------------------------
std = sqrt(variance)
print('Odchylenie standardowe:', std)

# cv --------------------------------------------
cv = std / abs(avarage) * 100
print('Wspolczynnik zmiennosci:', cv, '%')

# *****************************************************************
print(df_main)  # print dataframe with int values

df_row_sum = pd.DataFrame({'Fi': sum(Fi), 'FiXi': sum(FiXi), 'FiXi2': sum(FiXi2)}, 
    index=['sum']).fillna(0).astype(int).replace(np.nan, '-', regex=True)

print(df_row_sum)

df_main = df_main.append(df_row_sum)
# df_main = pd.DataFrame([df_row_sum])


# float to int

# pd_start_dict = pd_start_dict.fillna(0).astype(int)

# x = pd_start_dict.loc[['sum']].fillna(
#     0).astype(int).replace(0, '-', regex=True)
# pd_start_dict = pd_start_dict.append(x)
# print(df_main)
