import numpy as np
import pandas as pd
from itertools import accumulate
from math import sqrt

n = int(input('Wpisz rozmiar tablicy: '))
Xi = list(map(int, input(
    'Wpisz wartosci cechy (xi) oddzielone spacja: ').strip().split())
)[:n]
Fi = list(map(int, input(
    'Wpisz liczebnosci (fi) z jakimi te wartosci wystepuja: ').strip().split())
)[:n]

# Xi, Fi ---------------------------------------------------
start_dict = {'Xi': Xi, 'Fi': Fi}

# FiXi -----------------------------------------------------
FiXi = [i * j for i, j in zip(Xi, Fi)]
start_dict.update({'FiXi': FiXi})

# Xi2 ------------------------------------------------------
Xi2 = [i**2 for i in Xi]
start_dict.update({'Xi2': Xi2})

# FiXi2 ----------------------------------------------------
FiXi2 = [i * j for i, j in zip(Xi2, Fi)]
start_dict.update({'FiXi2': FiXi2})

# FiKu -----------------------------------------------------
FiKu = list(accumulate(Fi))
start_dict.update({'FiKu': FiKu})

# ???
# Detailed series ------------------------------------------
Detailed_series = []
for i, j in zip(Xi, Fi):
    count = 0
    while j != count:
        Detailed_series.append(i)
        count += 1
# print('Szereg szczegolowy:', Detailed_series)
dict_Detailed_series = {'Xi': Detailed_series}
pd_Detailed_series = pd.DataFrame(data=dict_Detailed_series, dtype=np.int64)
# print(pd_Detailed_series)
# ???

# Создаем фрейм ************************************************************************************
pd_start_dict = pd.DataFrame(data=start_dict, dtype=np.int64)
# print(pd_start_dict, '\n')

# Descriptive measures *****************************************************************************

# Mean ------------------------------------------
avarage = pd_start_dict.loc[:, 'FiXi'].sum() / sum(Fi)
print('Srednia arytmetyczna:', avarage)

# Median ----------------------------------------
median = pd_Detailed_series.loc[:, 'Xi'].median()
print('Mediana:', median)

# Mode ------------------------------------------
# mode = pd_Detailed_series['Xi'].mode()
mode = pd_Detailed_series.loc[:, 'Xi'].mode().values[0]
# mode.index = ['Mo: ']
print('Modalna:', mode)

# Variance --------------------------------------
variance = (1 / pd_start_dict.loc[:, 'Fi'].sum()) * \
    pd_start_dict.loc[:, 'FiXi2'].sum() - pow((avarage), 2)
print('Wariancja:', variance)

# std -------------------------------------------
std = sqrt(variance)
print('Odchylenie standardowe:', std)

# cv --------------------------------------------
cv = std / abs(avarage) * 100
print('Wspolczynnik zmiennosci:', cv, '%')

# *****************************************************************
print(pd_start_dict.fillna(0).astype(int))

row_sum = pd.Series({'Fi': sum(Fi), 'FiXi': sum(FiXi), 'FiXi2': sum(FiXi2)},
                    name='sum').fillna(
    0).astype(int).replace(0, '-', regex=True)

pd_start_dict = pd_start_dict.append(row_sum)

# float to int
# pd_start_dict = pd_start_dict.fillna(0).astype(int)

# x = pd_start_dict.loc[['sum']].fillna(
#     0).astype(int).replace(0, '-', regex=True)
# pd_start_dict = pd_start_dict.append(x)
print(pd_start_dict)
