import math
import os
import numpy as np
import pandas as pd
from itertools import accumulate
from pandas.core.algorithms import mode
from tabulate import tabulate
from decimal import Decimal


def toDecimal(num, n):
    num = Decimal(num)
    return round(num, n)


def display(df):
    print('\n')
    print(' ')
    print(tabulate(df, headers='keys', tablefmt='github'))


def run_point_series():
    print('\n')
    n = int(input('  Wpisz rozmiar tablicy: '))
    Xi = list(map(int, input(
        '  Wpisz wartosci cechy (xi) oddzielone spacja: ').strip().split()))[:n]
    print('\n')

    main_dict = {'Xi': Xi}
    df_prosty = pd.DataFrame(data=main_dict)

    average = df_prosty.mean()
    mode = df_prosty.mode()
    var = df_prosty.values.var()
    std = math.sqrt(var)

    df_descriptive_measures = pd.DataFrame(
        {},
        index=['miary statystyki']
    ).astype(np.float64)

    display(df_prosty)
    print('Average: ', average, '\n ', 'Mode: ', mode, '\n std: ', std)
    print('Var: ', var)
    # display(df_descriptive_measures)
    os.system('pause')


if __name__ == '__main__':
    run_point_series()
