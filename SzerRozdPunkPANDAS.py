import numpy as np
import pandas as pd
from itertools import accumulate

n = int(input('Wpisz rozmiar tablicy: '))
Xi = list(
    map(int, input('Wpisz wartosci cechy (xi) oddzielone spacja: ').strip().split())
)[:n]

Fi = list(
    map(int, input('Wpisz liczebnosci (fi) z jakimi te wartosci wystepuja: ').strip().split())
)[:n]

start_dict = {'Xi': Xi, 'Fi': Fi}

# FiXi -----------------------------------------------------
FiXi = [i * j for i, j in zip(Xi, Fi)]
start_dict.update({'FiXi': FiXi})

# Xi2 ------------------------------------------------------
Xi2 = [i**2 for i in Xi]

# FiXi2 ----------------------------------------------------
FiXi2 = [i * j for i, j in zip(Xi2, Fi)]
start_dict.update({'FiXi2': FiXi2})

# FiKu -----------------------------------------------------
FiKu = list(accumulate(Fi))
start_dict.update({'FiXi2': FiXi2})

# FiKu -----------------------------------------------------


# pd_start_dict = pd.DataFrame(data=start_dict)
# print(pd_start_dict)


# # Добавим все суммы в конце списка
# row_sum = pd.Series({'Fi': sum(Fi), 'FiXi2': sum(FiXi2)}, name='sum')
# pd_start_dict = pd_start_dict.append(row_sum)

# print(pd_start_dict)
