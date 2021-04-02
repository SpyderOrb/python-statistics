from collections import Counter
import operator
import math
import numpy as np


def suma(list):
    sum = 0
    for i in list:
        sum += i
    return sum


def arithmeticAverage(sum_FiXi, sum_Fi):
    return sum_FiXi / sum_Fi


def modalna(simpleXRow):
    dictSimpleXRow = dict(Counter(simpleXRow))
    modalna = max(dictSimpleXRow.items(), key=operator.itemgetter(1))[0]
    return modalna


def median(simpleXRow):
    x1 = simpleXRow[(sum_Fi + 1) // 2]
    x2 = 0.5 * (simpleXRow[(sum_Fi // 2)] + simpleXRow[(sum_Fi // 2 + 1)])
    if sum_Fi % 2 != 0:
        return x1
    else:
        return x2


def variance(sum_Fi, sum_FiXi2, arithmeticAverage):
    s2 = (1 / sum_Fi) * sum_FiXi2 - (arithmeticAverage)**2
    return s2


def standardDeviation(variance):
    return variance ** 0.5


def coefficientOfVariation(standardDeviation, arithmeticAverage):
    Vs = standardDeviation / abs(arithmeticAverage) * 100
    return Vs


n = int(input('Wpisz rozmiar tablicy: '))
Xi = list(
    map(int, input('Wpisz wartosci cechy (xi) oddzielone spacja: ').strip().split())
)[:n]

Fi = list(
    map(int, input('Wpisz liczebnosci (fi) z jakimi te wartosci wystepuja: ').strip().split())
)[:n]

print('\n')

sum_Fi = suma(Fi)

FiXi = []
for i, j in zip(Xi, Fi):
    FiXi.append(i * j)

sum_FiXi = suma(FiXi)

Xi2 = []
for i in Xi:
    Xi2.append(i**2)

FiXi2 = []
for i, j in zip(Xi2, Fi):
    FiXi2.append(i * j)

sum_FiXi2 = suma(FiXi2)

FiKu = []
FiKu_total = 0
for i in Fi:
    FiKu_total += i
    FiKu.append(FiKu_total)

simpleXRow = []
for i, j in zip(Xi, Fi):
    count = 0
    while (j != count):
        simpleXRow.append(i)
        count += 1

modalna = modalna(simpleXRow)
arithmeticAverage = arithmeticAverage(sum_FiXi, sum_Fi)
median = median(simpleXRow)
variance = variance(sum_Fi, sum_FiXi2, arithmeticAverage)
standardDeviation = standardDeviation(variance)
coefficientOfVariation = coefficientOfVariation(
    standardDeviation, arithmeticAverage)

print(f'Wartosci cechy: {Xi}', f'Liczebnosc: {Fi}', f'Suma liczebnosci: {sum_Fi}',
      f'Wartosc fi * xi: {FiXi}', f'Suma fi * xi: {sum_FiXi}', f'Wartosc xi^2: {Xi2}',
      f'Wartosc fi * xi^2: {FiXi2}', f'Suma fi * xi^2: {sum_FiXi2}', f'Wartosc fi skumulowana: {FiKu}',
      f'Szereg szczegolowy: {simpleXRow} \n', f'Srednia arytmetyczna: {arithmeticAverage}', f'Modalna: {modalna}',
      f'Mediana: {median}', f'Wariancja: {variance}', f'Odchylenie standardowe: {standardDeviation}',
      f'Wspolczynnik zmiennosci: {coefficientOfVariation}%', sep='\n')
