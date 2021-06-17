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


if __name__ == "__main__":
    run_measures_interdependence()
