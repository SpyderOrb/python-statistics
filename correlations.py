from interval_series import toDecimal
import math
import os
import numpy as np
from numpy.lib import median
import pandas as pd
from itertools import accumulate, product
from tabulate import tabulate
from decimal import Decimal


def sign(b):
    if (b > 0):
        return '+'
    return '-'


def toRoundDecimal(num, n=4):
    num = Decimal(num)
    return round(num, n)


def display(df):
    print(' ')
    print(tabulate(df, headers='keys', tablefmt='github'))
    print(end='\n')


def run_correlations():
    # Współczynnik korelacji (korelogram)

    n = int(input('  Wpisz rozmiar tablicy: '))
    Xi = list(map(int, input(
        '  Wpisz wartosc cechy Xi oddzielone spacja: ').strip().split()))[:n]
    Yi = list(map(int, input(
        '  Wpisz wartosc cechy Yi oddzielone spacja: ').strip().split()))[:n]
    decimal_places = int(
        input('  Ile chcesz miec miejsc po pzecinku (wartosc domyslna to 4): ') or "4")

    # Xi = [16, 25, 24, 50, 60]
    # Yi = [95, 163, 250, 297, 335]

    # Сreating a dataframe
    df_correlation = pd.DataFrame(list(zip(Xi, Yi)), columns=['Xi', 'Yi'])

    # Xi, Yi averages -----------------------------------------------------
    # ---------------------------------------------------------------------
    Xi_avg = round(df_correlation.loc[:, 'Xi'].mean(), decimal_places)
    Yi_avg = round(df_correlation.loc[:, 'Yi'].mean(), decimal_places)

    # Xi - Xi_avg, Yi - Yi_avg, -------------------------------------------
    Xi_diff_Xi_avg = [(i - Xi_avg) for i in Xi]
    Yi_diff_Yi_avg = [(i - Yi_avg) for i in Yi]
    df_correlation['Xi-Xi_avg'] = Xi_diff_Xi_avg
    df_correlation['Yi-Yi_avg'] = Yi_diff_Yi_avg

    # (Xi - Xi_avg) * (Yi - Yi_avg) ---------------------------------------
    Xi_diff_Xi_avg_MULT_Yi_diff_Yi_avg = [
        round(i * j, decimal_places) for i, j in zip(Xi_diff_Xi_avg, Yi_diff_Yi_avg)]
    df_correlation['(Xi-Xi_avg)(Yi-Yi_avg)'] = Xi_diff_Xi_avg_MULT_Yi_diff_Yi_avg

    # (Xi - Xi_avg)^2, (Yi - Yi_avg)^2 ------------------------------------
    Xi_diff_Xi_avg2 = [round(i ** 2, decimal_places) for i in Xi_diff_Xi_avg]
    Yi_diff_Yi_avg2 = [round(i ** 2, decimal_places) for i in Yi_diff_Yi_avg]
    df_correlation['(Xi-Xi_avg)^2'] = Xi_diff_Xi_avg2
    df_correlation['(Yi-Yi_avg)^2'] = Yi_diff_Yi_avg2

    # Descriptive measures ********************************************************************************
    # Pearson linear correlation coefficient-------------------------------
    r = (sum(Xi_diff_Xi_avg_MULT_Yi_diff_Yi_avg) /
         (math.sqrt(sum(Xi_diff_Xi_avg2) * sum(Yi_diff_Yi_avg2))))

    # Wyraz wolny (a) i wsp regresji (b)-----------------------------------
    b = (sum(Xi_diff_Xi_avg_MULT_Yi_diff_Yi_avg) / sum(Xi_diff_Xi_avg2))
    a = Yi_avg - b * Xi_avg

    # Zmiana wartosci cechy ΔX---------------------------------------------
    print('  Chcesz podac zmiany wartosci cechy ΔX (wpisz 0 jezeli nie chcech):', end=' ')
    deltaX = float(input() or "0")
    if (deltaX != 0):
        deltaY = b * deltaX
        deltaYr = toRoundDecimal(deltaY, decimal_places)
    else:
        deltaYr = 'skipped...'

    # Prognozowanie -------------------------------------------------------
    print('  Wpisz wartosc predykatora X* (wpisz 0 jezeli nie chcech):', end=' ')
    Xpredictor = float(input() or "0")
    if (Xpredictor != 0):
        Ypredictor = a + b * Xpredictor
        YpredictorR = toRoundDecimal(Ypredictor, decimal_places)
    else:
        YpredictorR = 'skipped...'

    # ŷ, Yi - ŷ, (Yi - ŷ)^2 -----------------------------------------------
    Yteoretyczne = [round((a + b * i), decimal_places) for i in Xi]
    df_correlation['ŷ'] = Yteoretyczne
    Yi_diff_Yteoretyczne = [(i - j) for i, j in zip(Yi, Yteoretyczne)]
    Yi_diff_Yteoretyczne2 = [round(i ** 2, decimal_places)
                             for i in Yi_diff_Yteoretyczne]
    df_correlation['(Yi - ŷ)^2'] = Yi_diff_Yteoretyczne2
    # Wariancja resztowa --------------------------------------------------
    Se2 = (1/(n-2) * sum(Yi_diff_Yteoretyczne2))

    # Odchylenie standardowe reszt ----------------------------------------
    std = math.sqrt(Se2)

    # Współczynnik zmienności resztowej -----------------------------------
    cv = std / abs(Yi_avg) * 100
    if (cv < 10):
        cv_message = '  Vse < 10%.  Ten model jest dobrze dopasowany do danych.'
    else:
        cv_message = '  Vse > 10%.  Ten model jest slabo dopasowany do danych.'

    # Współczynnik zbieżności (indeterminacji) ----------------------------
    oIo2 = sum(Yi_diff_Yteoretyczne2) / sum(Yi_diff_Yi_avg2)
    oIo2_proc = oIo2 * 100

    # Współczynnik determinacji -------------------------------------------
    R2 = 1 - oIo2
    R2_proc = R2 * 100

    # Dataframes
    df_correlation_row_sum = pd.DataFrame(
        {'(Xi-Xi_avg)(Yi-Yi_avg)': toRoundDecimal(sum(Xi_diff_Xi_avg_MULT_Yi_diff_Yi_avg), decimal_places),
         '(Xi-Xi_avg)^2': toRoundDecimal(sum(Xi_diff_Xi_avg2), decimal_places),
         '(Yi-Yi_avg)^2': toRoundDecimal(sum(Yi_diff_Yi_avg2), decimal_places),
         '(Yi - ŷ)^2': toRoundDecimal(sum(Yi_diff_Yteoretyczne2), decimal_places)
         },
        index=['sum']
    )

    df_correlation_descriptive_measures = pd.DataFrame(
        {'wsp korelacji (r)': toRoundDecimal(r, decimal_places),
         'wsp regresji (b)': toRoundDecimal(b, decimal_places),
         'wyraz wolny (a)': toRoundDecimal(a, decimal_places),
         'Se^2': toRoundDecimal(Se2, decimal_places),
         'Se': toRoundDecimal(std, decimal_places),
         'Vse (%)': toRoundDecimal(cv, decimal_places),
         'φ^2 (%)': toRoundDecimal(oIo2_proc, decimal_places),
         'R^2 (%)': toRoundDecimal(R2_proc, decimal_places)
         },
        index=['miary statystyki']
    ).astype(np.float64)

    display(df_correlation)
    print(f'  Xi srednia:  {Xi_avg} | Yi srednia: {Yi_avg}')
    display(df_correlation_row_sum)
    print(
        f'  Rownanie regresji: Y = {toRoundDecimal(a, decimal_places)} {sign(b)} {toRoundDecimal(b, decimal_places)} * X')
    display(df_correlation_descriptive_measures)
    print(cv_message)
    print('  ΔY: ', deltaYr)
    print('  *X: ', YpredictorR)


if __name__ == "__main__":
    run_correlations()
