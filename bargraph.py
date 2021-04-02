# import matplotlib.pyplot as plt

# x_list = list(range(0, 5))
# y1_list = [22, 17, 81, 41, 25]

# plt.plot(x_list, y1_list)
# plt.show()

n = int(input('Wpisz rozmiar tablicy:'))
Xi = list(
    map(int, input('Wpisz wartosci cechy (xi) oddzielone spacja:').strip().split())
)[:n]

Fi = list(
    map(int, input('Wpisz liczebnosci (fi) z jakimi te wartosci wystepuja:').strip().split())
)[:n]

print('\n')
print('Wartosci cechy:', Xi)
print('Liczebnosc:', Fi)
