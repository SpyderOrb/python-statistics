# Techniki wyodrębniania trendu w szeregach czasowych
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


def run_isolating_trend():
    t = int(input('  Wpisz numer ostatniego okesu t: '))
    t_list = list(range(1, t+1))
    year1 = int(input(
        '  Wpisz pierwszy rok (lub numer misiaca itd): '))
    years_list = list(range(year1, year1+t))
    Yt = list(map(int, input(
        '  Wpisz wartosc cechy Yt oddzielone spacja: ').strip().split()))[:t]
    decimal_places = int(
        input('  Ile chcesz miec miejsc po pzecinku (wartosc domyslna to 4): ') or "4")

    # Yt = [50, 52, 45, 62, 69, 50, 72, 75]

    # Сreating a dataframe
    df_correlation = pd.DataFrame({'t': t_list, 'Czas': years_list, 'Yt': Yt})

    # Yt, t average -----------------------------------------------------
    # ---------------------------------------------------------------------
    Yt_avg = df_correlation.loc[:, 'Yt'].mean()
    t_avg = df_correlation.loc[:, 't'].mean()

    # t - t_avg, Yt - Yt_avg, -------------------------------------------
    t_diff_t_avg = [(i - t_avg) for i in t_list]
    Yt_diff_Yt_avg = [(i - Yt_avg) for i in Yt]
    df_correlation['t-t_avg'] = t_diff_t_avg
    df_correlation['Yt-Yt_avg'] = Yt_diff_Yt_avg

    # (t - t_avg) * (Yt - Yt_avg) ---------------------------------------
    t_diff_t_avg_MULT_Yt_diff_Yt_avg = [
        i * j for i, j in zip(t_diff_t_avg, Yt_diff_Yt_avg)]
    df_correlation['(t-t_avg)(Yt-Yt_avg)'] = t_diff_t_avg_MULT_Yt_diff_Yt_avg

    # (t - t_avg)^2 ------------------------------------
    t_diff_t_avg2 = [i ** 2 for i in t_diff_t_avg]
    df_correlation['(t-t_avg)^2'] = t_diff_t_avg2

    # Descriptive measures ********************************************************************************
    # # Pearson linear correlation coefficient-------------------------------
    # r = (sum(Xi_diff_Xi_avg_MULT_Yi_diff_Yi_avg) /
    #      (math.sqrt(sum(Xi_diff_Xi_avg2) * sum(Yi_diff_Yi_avg2))))

    # Parametr (a) i wsp trendu (b)-----------------------------------
    b = (sum(t_diff_t_avg_MULT_Yt_diff_Yt_avg) / sum(t_diff_t_avg2))
    a = Yt_avg - b * t_avg

    # # Zmiana wartosci cechy ΔX---------------------------------------------
    # print('  Chcesz podac zmiany wartosci cechy ΔX (wpisz 0 jezeli nie chcech):', end=' ')
    # deltaX = int(input() or "0")
    # if (deltaX != 0):
    #     deltaY = b * deltaX
    #     deltaYr = toRoundDecimal(deltaY, decimal_places)
    # else:
    #     deltaYr = 'skipped...'

    # Prognozowanie -------------------------------------------------------
    print('  Wpisz numer okresu prognozy T (wpisz 0 jezeli nie chcesz):', end=' ')
    Tpredictor = int(input() or "0")
    if (Tpredictor != 0):
        Yt_predictor = a + b * Tpredictor
        Yt_predictorR = toRoundDecimal(Yt_predictor, decimal_places)
    else:
        Yt_predictorR = 'skipped...'

    # ŷt, Yt - ŷt, (Yt - ŷt)^2, (Yt - Y_avg)^2 -----------------------------------------------
    Yt_teoretyczne = [(a + b * i) for i in t_list]
    df_correlation['ŷt'] = Yt_teoretyczne

    Yt_diff_Yt_teoretyczne = [(i - j) for i, j in zip(Yt, Yt_teoretyczne)]
    Yt_diff_Yt_teoretyczne2 = [i ** 2 for i in Yt_diff_Yt_teoretyczne]
    df_correlation['(Yt - ŷ)^2'] = Yt_diff_Yt_teoretyczne2

    Yt_diff_Yt_avg2 = [i ** 2 for i in Yt_diff_Yt_avg]
    df_correlation['(Yt - Yt_avg)^2'] = Yt_diff_Yt_avg2

    # Wariancja resztowa --------------------------------------------------
    Se2 = (1/(t-2) * sum(Yt_diff_Yt_teoretyczne2))

    # Odchylenie standardowe reszt ----------------------------------------
    std = math.sqrt(Se2)

    # Współczynnik zmienności resztowej -----------------------------------
    cv = std / abs(Yt_avg) * 100
    if (cv < 10):
        cv_message = '  Vse < 10%.  Ten model jest dobrze dopasowany do danych.'
    else:
        cv_message = '  Vse > 10%.  Ten model jest slabo dopasowany do danych.'

    # Współczynnik zbieżności (indeterminacji) ----------------------------
    oIo2 = sum(Yt_diff_Yt_teoretyczne2) / sum(Yt_diff_Yt_avg2)
    oIo2_proc = oIo2 * 100

    # Współczynnik determinacji -------------------------------------------
    R2 = 1 - oIo2
    R2_proc = R2 * 100

    # Dataframes
    df_correlation_row_sum = pd.DataFrame(
        {'t': sum(t_list),
         'Yt': sum(Yt),
         '(t - t_avg)(Yt - Yt_avg)': sum(t_diff_t_avg_MULT_Yt_diff_Yt_avg),
         '(t - t_avg)^2': sum(t_diff_t_avg2),
         '(Yt - ŷt)^2': sum(Yt_diff_Yt_teoretyczne2),
         '(Yt - Yt_avg)^2': sum(Yt_diff_Yt_avg2)
         },
        index=['sum']
    )

    df_correlation_descriptive_measures = pd.DataFrame(
        {'wsp trendu (b)': toRoundDecimal(b, decimal_places),
         'parametr (a)': toRoundDecimal(a, decimal_places),
         'Se^2': toRoundDecimal(Se2, decimal_places),
         'Se': toRoundDecimal(std, decimal_places),
         'Vse (%)': toRoundDecimal(cv, decimal_places),
         'φ^2 (%)': toRoundDecimal(oIo2_proc, decimal_places),
         'R^2 (%)': toRoundDecimal(R2_proc, decimal_places)
         },
        index=['miary statystyki']
    ).astype(np.float64)

    display(df_correlation)
    print(f'  t srednia:  {t_avg} | Yt srednia: {Yt_avg}')
    display(df_correlation_row_sum)
    print(
        f'  Funkcja trendu: Y = {toRoundDecimal(a, decimal_places)} {sign(b)} {toRoundDecimal(b, decimal_places)} * t')
    display(df_correlation_descriptive_measures)
    print(cv_message)
    # print('  ΔY: ', deltaYr)
    print('  Yp: ', Yt_predictorR)


if __name__ == "__main__":
    run_isolating_trend()
