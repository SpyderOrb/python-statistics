import math
import os
import numpy as np
from numpy.lib import median
import pandas as pd
from itertools import accumulate, product
from tabulate import tabulate


def sign(b):
    if (b > 0):
        return '+'
    return '-'


def display(df):
    print(' ')
    print(tabulate(df, headers='keys', tablefmt='github'))
    print('\n')


def run_correlations():
    # Współczynnik korelacji (korelogram)
    # Liniowa funkcja regresji

    n = int(input('Wpisz rozmiar tablicy: '))
    Xi = list(map(int, input(
        'Wpisz wartosc cechy Xi oddzielone spacja: ').strip().split()))[:n]
    Yi = list(map(int, input(
        'Wpisz wartosc cechy Yi oddzielone spacja: ').strip().split()))[:n]
    # Xi = [16, 25, 24, 50, 60]
    # Yi = [95, 163, 250, 297, 335]

    df_correlation = pd.DataFrame(list(zip(Xi, Yi)), columns=['Xi', 'Yi'])
    # Xi, Yi averages -----------------------------------------------------
    Xi_avg = df_correlation.loc[:, 'Xi'].mean()
    Yi_avg = df_correlation.loc[:, 'Yi'].mean()

    # Xi - Xi_avg, Yi - Yi_avg --------------------------------------------
    Xi_diff_Xi_avg = [(i - Xi_avg) for i in Xi]
    Yi_diff_Yi_avg = [(i - Yi_avg) for i in Yi]
    df_correlation['Xi-Xi_avg'] = Xi_diff_Xi_avg
    df_correlation['Yi-Yi_avg'] = Yi_diff_Yi_avg

    # (Xi - Xi_avg) * (Yi - Yi_avg) ---------------------------------------
    Xi_diff_Xi_avg_MULT_Yi_diff_Yi_avg = [
        i * j for i, j in zip(Xi_diff_Xi_avg, Yi_diff_Yi_avg)]
    df_correlation['(Xi-Xi_avg)(Yi-Yi_avg)'] = Xi_diff_Xi_avg_MULT_Yi_diff_Yi_avg

    # (Xi - Xi_avg)^2, (Yi - Yi_avg)^2 ------------------------------------
    Xi_diff_Xi_avg2 = [i ** 2 for i in Xi_diff_Xi_avg]
    Yi_diff_Yi_avg2 = [i ** 2 for i in Yi_diff_Yi_avg]
    df_correlation['(Xi-Xi_avg)^2'] = Xi_diff_Xi_avg2
    df_correlation['(Yi-Yi_avg)^2'] = Yi_diff_Yi_avg2

    df_correlation_row_sum = pd.DataFrame(
        {'(Xi-Xi_avg)(Yi-Yi_avg)': sum(Xi_diff_Xi_avg_MULT_Yi_diff_Yi_avg),
         '(Xi-Xi_avg)^2': sum(Xi_diff_Xi_avg2),
         '(Yi-Yi_avg)^2': sum(Yi_diff_Yi_avg2)
         },
        index=['sum']
    )

    # Pearson linear correlation coefficient-------------------------------
    r = round((sum(Xi_diff_Xi_avg_MULT_Yi_diff_Yi_avg) /
               (math.sqrt(sum(Xi_diff_Xi_avg2) * sum(Yi_diff_Yi_avg2)))), 2)

    # Wyraz wolny (a) i wsp regresji (b)-----------------------------------
    b = round((sum(Xi_diff_Xi_avg_MULT_Yi_diff_Yi_avg) / sum(Xi_diff_Xi_avg2)), 2)
    a = round(Yi_avg - b * Xi_avg, 2)

    #

    df_correlation_descriptive_measures = pd.DataFrame(
        {'wsp korelacji (r)': r,
         'wsp regresji (b)': b,
         'wyraz wolny (a)': a
         },
        index=['miary statystyki']
    ).astype(np.float64)

    display(df_correlation)
    print(f'Xi srednia:  {Xi_avg} | Yi srednia: {Yi_avg}')
    display(df_correlation_row_sum)
    display(df_correlation_descriptive_measures)
    print(f'Rownanie regresji: Y = {a} {sign(b)} {b} * X')

    os.system('pause')


if __name__ == "__main__":
    run_correlations()
