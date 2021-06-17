# Techniki wyodrębniania trendu w szeregach czasowych
from numpy.matrixlib import matrix
from interval_series import toDecimal
import math
import os
import numpy as np
from numpy.lib import append, median
import pandas as pd
from itertools import accumulate, chain, product
from tabulate import tabulate
from decimal import Decimal, ROUND_HALF_DOWN


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


def run_measures_interdependence():

    # w = int(input("Wpisz ilość wiersz: "))
    # k = int(input("Wpisz ilosc kolumn: "))
    # matrix_list = [[int(input(f"Wpisz wartosc dla (wiersz)-{i+1} (kolumna)-{j+1}: "))
    #                 for j in range(k)] for i in range(w)]

    #
    decimal_places = int(
        input('  Ile chcesz miec miejsc po pzecinku (wartosc domyslna to 4): ') or "4")
    w = 3
    k = 2
    matrix_list = [[360, 164], [308, 75], [132, 36]]
    #

    df_matrix = pd.DataFrame()

    matrix_np = np.matrix(matrix_list)
    matrix_np_one = np.matrix(matrix_list)

    n_i_kropka = np.sum(matrix_np, axis=1)
    # [524, 383, 168]
    # print(n_i_kropka)
    n = sum(n_i_kropka)
    # [1075]

    n_kropka_j = np.sum(matrix_np, axis=0)
    n_kropka_j_old = n_kropka_j
    n_kropka_j = np.append(n_kropka_j, n, axis=1)
    # [[ 800  275 1075]]
    # print(n_kropka_j)

    matrix_np = np.append(matrix_np, n_i_kropka, axis=1)
    matrix_np = np.append(matrix_np, n_kropka_j, axis=0)

    df_matrix = pd.concat([df_matrix, pd.DataFrame(matrix_np)], axis=1)
    df_matrix.rename({df_matrix.index[-1]: 'n.j'}, inplace=True)
    df_matrix.columns = [*df_matrix.columns[:-1], 'ni.']
    display(df_matrix)

    # nij i declare Dataframe -----------------------
    df_matrix_tab = pd.DataFrame()

    nij = list(chain.from_iterable(matrix_list))
    df_matrix_tab['nij'] = nij

    # ňij
    nij_teorytyczne = []
    for i in n_i_kropka:
        for j in n_kropka_j_old:
            result = np.round(((i * j) / n), decimal_places)
            nij_teorytyczne = np.append(nij_teorytyczne, result)

    df_matrix_tab['ňij'] = nij_teorytyczne

    # (nij - ňij)^2
    nij_diff_nij_teoretyczne2 = []
    for i, j in zip(nij, nij_teorytyczne):
        nij_diff_nij_teoretyczne2.append(round(pow((i-j), 2), decimal_places))

    df_matrix_tab['(nij - ňij)^2'] = nij_diff_nij_teoretyczne2

    # (nij - ňij)^2 / ňij
    nij_diff_nij_teoretyczne2_DIV_nij_teoretyczne = []
    for i, j in zip(nij_diff_nij_teoretyczne2, nij_teorytyczne):
        nij_diff_nij_teoretyczne2_DIV_nij_teoretyczne.append(
            round(i/j, decimal_places))

    df_matrix_tab['(nij - ňij)^2 / ňij'] = nij_diff_nij_teoretyczne2_DIV_nij_teoretyczne

    # chi-kwadrat
    Chi2 = sum(nij_diff_nij_teoretyczne2_DIV_nij_teoretyczne)

    # Wsp Yule'a φ^2
    φ = math.sqrt(Chi2/n)

    # Wsp V-Cramera
    VCramera = math.sqrt(Chi2 / (n * min((k-1), (w-1))))

    # Wsp T-Czuprowa
    TCzuprowa = math.sqrt(Chi2 / (n * math.sqrt((k-1)*(w-1))))

    df_matrix_descriptive_measures = pd.DataFrame(
        {'Chi-kwadrat X^2': toRoundDecimal(Chi2, decimal_places),
         'φ': toRoundDecimal(φ, decimal_places),
         'V-Cramera': toRoundDecimal(VCramera, decimal_places),
         'T-Czuprowa': toRoundDecimal(TCzuprowa, decimal_places)
         },
        index=['miary statystyki']
    ).astype(np.float64)

    display(df_matrix_tab)
    display(df_matrix_descriptive_measures)

    # n_i_kropka = [[for j in range(k)] for i in range(k)]
    # print(n_i_kropka)
    # t = int(input('  Wpisz numer ostatniego okesu t: '))
    # t_list = list(range(1, t+1))
    # year1 = int(input(
    #     '  Wpisz pierwszy rok (lub numer misiaca itd): '))
    # years_list = list(range(year1, year1+t))
    # Yt = list(map(int, input(
    #     '  Wpisz wartosc cechy Yt oddzielone spacja: ').strip().split()))[:t]
    # decimal_places = int(
    #     input('  Ile chcesz miec miejsc po pzecinku (wartosc domyslna to 4): ') or "4")

    # # Yt = [50, 52, 45, 62, 69, 50, 72, 75]

    # # Сreating a dataframe
    # df_correlation = pd.DataFrame({'t': t_list, 'Czas': years_list, 'Yt': Yt})

    # # Yt, t average -----------------------------------------------------
    # # ---------------------------------------------------------------------
    # Yt_avg = round(df_correlation.loc[:, 'Yt'].mean(), decimal_places)
    # t_avg = df_correlation.loc[:, 't'].mean()

    # # t - t_avg, Yt - Yt_avg, -------------------------------------------
    # t_diff_t_avg = [round((i - t_avg), decimal_places) for i in t_list]
    # Yt_diff_Yt_avg = [round((i - Yt_avg), decimal_places) for i in Yt]
    # df_correlation['t-t_avg'] = t_diff_t_avg
    # df_correlation['Yt-Yt_avg'] = Yt_diff_Yt_avg

    # # (t - t_avg) * (Yt - Yt_avg) ---------------------------------------
    # t_diff_t_avg_MULT_Yt_diff_Yt_avg = [
    #     round(i * j, decimal_places) for i, j in zip(t_diff_t_avg, Yt_diff_Yt_avg)]
    # df_correlation['(t-t_avg)(Yt-Yt_avg)'] = t_diff_t_avg_MULT_Yt_diff_Yt_avg

    # # (t - t_avg)^2 ------------------------------------
    # t_diff_t_avg2 = [round((i ** 2), decimal_places) for i in t_diff_t_avg]
    # df_correlation['(t-t_avg)^2'] = t_diff_t_avg2

    # # Descriptive measures ********************************************************************************
    # # # Pearson linear correlation coefficient-------------------------------
    # # r = (sum(Xi_diff_Xi_avg_MULT_Yi_diff_Yi_avg) /
    # #      (math.sqrt(sum(Xi_diff_Xi_avg2) * sum(Yi_diff_Yi_avg2))))

    # # Parametr (a) i wsp trendu (b)-----------------------------------
    # b = (sum(t_diff_t_avg_MULT_Yt_diff_Yt_avg) / sum(t_diff_t_avg2))
    # a = Yt_avg - b * t_avg

    # # # Zmiana wartosci cechy ΔX---------------------------------------------
    # # print('  Chcesz podac zmiany wartosci cechy ΔX (wpisz 0 jezeli nie chcech):', end=' ')
    # # deltaX = int(input() or "0")
    # # if (deltaX != 0):
    # #     deltaY = b * deltaX
    # #     deltaYr = toRoundDecimal(deltaY, decimal_places)
    # # else:
    # #     deltaYr = 'skipped...'

    # # Prognozowanie -------------------------------------------------------
    # print('  Wpisz numer okresu prognozy T (wpisz 0 jezeli nie chcesz):', end=' ')
    # Tpredictor = int(input() or "0")
    # if (Tpredictor != 0):
    #     Yt_predictor = a + b * Tpredictor
    #     Yt_predictorR = toRoundDecimal(Yt_predictor, decimal_places)
    # else:
    #     Yt_predictorR = 'skipped...'

    # # ŷt, Yt - ŷt, (Yt - ŷt)^2, (Yt - Y_avg)^2 -----------------------------------------------
    # Yt_teoretyczne = [round((a + b * i), decimal_places) for i in t_list]
    # df_correlation['ŷt'] = Yt_teoretyczne

    # Yt_diff_Yt_teoretyczne = [(i - j) for i, j in zip(Yt, Yt_teoretyczne)]
    # Yt_diff_Yt_teoretyczne2 = [
    #     round((i ** 2), decimal_places) for i in Yt_diff_Yt_teoretyczne]
    # df_correlation['(Yt - ŷ)^2'] = Yt_diff_Yt_teoretyczne2

    # Yt_diff_Yt_avg2 = [round((i ** 2), decimal_places) for i in Yt_diff_Yt_avg]
    # df_correlation['(Yt - Yt_avg)^2'] = Yt_diff_Yt_avg2

    # # Wariancja resztowa --------------------------------------------------
    # Se2 = (1/(t-2) * sum(Yt_diff_Yt_teoretyczne2))

    # # Odchylenie standardowe reszt ----------------------------------------
    # std = math.sqrt(Se2)

    # # Współczynnik zmienności resztowej -----------------------------------
    # cv = std / abs(Yt_avg) * 100
    # if (cv < 10):
    #     cv_message = '  Vse < 10%.  Ten model jest dobrze dopasowany do danych.'
    # else:
    #     cv_message = '  Vse > 10%.  Ten model jest slabo dopasowany do danych.'

    # # Współczynnik zbieżności (indeterminacji) ----------------------------
    # oIo2 = sum(Yt_diff_Yt_teoretyczne2) / sum(Yt_diff_Yt_avg2)
    # oIo2_proc = oIo2 * 100

    # # Współczynnik determinacji -------------------------------------------
    # R2 = 1 - oIo2
    # R2_proc = R2 * 100

    # # Dataframes
    # df_correlation_row_sum = pd.DataFrame(
    #     {'t': sum(t_list),
    #      'Yt': sum(Yt),
    #      '(t - t_avg)(Yt - Yt_avg)': sum(t_diff_t_avg_MULT_Yt_diff_Yt_avg),
    #      '(t - t_avg)^2': sum(t_diff_t_avg2),
    #      '(Yt - ŷt)^2': sum(Yt_diff_Yt_teoretyczne2),
    #      '(Yt - Yt_avg)^2': sum(Yt_diff_Yt_avg2)
    #      },
    #     index=['sum']
    # )

    # df_correlation_descriptive_measures = pd.DataFrame(
    #     {'wsp trendu (b)': toRoundDecimal(b, decimal_places),
    #      'parametr (a)': toRoundDecimal(a, decimal_places),
    #      'Se^2': toRoundDecimal(Se2, decimal_places),
    #      'Se': toRoundDecimal(std, decimal_places),
    #      'Vse (%)': toRoundDecimal(cv, decimal_places),
    #      'φ^2 (%)': toRoundDecimal(oIo2_proc, decimal_places),
    #      'R^2 (%)': toRoundDecimal(R2_proc, decimal_places)
    #      },
    #     index=['miary statystyki']
    # ).astype(np.float64)

    # display(df_correlation)
    # print(f'  t srednia:  {t_avg} | Yt srednia: {Yt_avg}')
    # display(df_correlation_row_sum)
    # print(
    #     f'  Funkcja trendu: Y = {toRoundDecimal(a, decimal_places)} {sign(b)} {toRoundDecimal(b, decimal_places)} * t')
    # display(df_correlation_descriptive_measures)
    # print(cv_message)
    # # print('  ΔY: ', deltaYr)
    # print('  Yp: ', Yt_predictorR)


if __name__ == "__main__":
    run_measures_interdependence()
