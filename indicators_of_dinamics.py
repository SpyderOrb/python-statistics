# Indywidualne wskaźniki dynamiki
from isolating_trend import run_isolating_trend
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


def run_indicators_of_dinamics():
    t = int(input('  Wpisz numer ostatniego indeksu t: '))
    t_list = list(range(1, t+1))
    year1 = int(input(
        '  Wpisz pierwszy rok (lub numer misiaca itd): '))
    years_list = list(range(year1, year1+t))
    Yt = list(map(int, input(
        '  Wpisz wartosc cechy Yt oddzielone spacja: ').strip().split()))[:t]
    decimal_places = int(
        input('  Ile chcesz miec miejsc po pzecinku (wartosc domyslna to 4): ') or "4")

    # Creating a dataframe
    df_dynamics_of_phenomena = pd.DataFrame(
        {'t': t_list, 'Czas': years_list, 'Yt': Yt})
    # --------------------------------------------------------------------
    # yt - y0 ------------------------------------------------------------
    yt_diff_t0 = [round((Yt[i] - Yt[0]), decimal_places)
                  for i in range(len(Yt))]
    df_dynamics_of_phenomena['yt - y0'] = yt_diff_t0
    # yt - yt-1 ----------------------------------------------------------
    yt_diff_tMinus1 = [round((Yt[i] - Yt[i-1])) for i in range(len(Yt))]
    yt_diff_tMinus1[0] = np.nan
    df_dynamics_of_phenomena['yt - yt-1'] = yt_diff_tMinus1
    # (yt - y0) / y0 * 100 -----------------------------------------------
    yt_diff_t0_div_t0 = [round(((Yt[i] - Yt[0])/Yt[0] * 100))
                         for i in range(len(Yt))]
    df_dynamics_of_phenomena['(yt - y0)/y0 * 100'] = yt_diff_t0_div_t0
    # (yt - yt-1) / yt-1 * 100 -------------------------------------------
    yt_diff_tMinus1_div_tMinus1 = [
        round(((Yt[i] - Yt[i-1])/Yt[i-1] * 100)) for i in range(len(Yt))]
    yt_diff_tMinus1_div_tMinus1[0] = np.nan
    df_dynamics_of_phenomena['(yt - yt-1)/yt-1 * 100'] = yt_diff_tMinus1_div_tMinus1
    # yt / y0 * 100 ------------------------------------------------------
    yt_div_y0 = [round((Yt[i]/Yt[0] * 100), decimal_places)
                 for i in range(len(Yt))]
    df_dynamics_of_phenomena['yt / y0 * 100'] = yt_div_y0
    # yt / yt-1 * 100 ----------------------------------------------------
    yt_div_yMinus1 = [round((Yt[i]/Yt[i-1] * 100), decimal_places)
                      for i in range(len(Yt))]
    yt_div_yMinus1[0] = np.nan
    df_dynamics_of_phenomena['yt / yt-1 * 100'] = yt_div_yMinus1

    # Average rate of changes of the phenomenon over time ----------------
    G = pow((Yt[t-1] / Yt[0]), 1/(t-1))
    G_proc = (1 - G) * 100
    if (G_proc > 0):
        say_something = "zwiekszyly"
    else:
        say_something = "zmniejszyly"

    # Prediction
    print('  Wpisz numer okresu prognozy T (wpisz 0 jezeli nie chcesz):', end=' ')
    Tpredictor = int(input() or "0")
    if (Tpredictor != 0):
        h = Tpredictor - t
        Yt_predictor = pow(G, h) * Yt[t-1]
        Yt_predictorR = toRoundDecimal(Yt_predictor, decimal_places)
    else:
        Yt_predictorR = 'skipped...'

    df_dynamics_of_phenomena_descriptive_measures = pd.DataFrame(
        {
            'G(srednie tempo zmian)': toRoundDecimal(G, decimal_places),
            'G(srednie tempo zmian) (%)': toRoundDecimal(G_proc, decimal_places)
        },
        index=['miary statystyki']
    )

    display(df_dynamics_of_phenomena)
    display(df_dynamics_of_phenomena_descriptive_measures)
    print(
        f'  Interpretacja G: Z roku na rok w latah {years_list[0]}-{years_list[-1]} (...wpisz tu znaczenie Yt) {say_something} sie srednio ok. {G_proc}.')
    print('  Yp: ', Yt_predictorR)


if __name__ == "__main__":
    run_indicators_of_dinamics()
