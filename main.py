import os
import point_series
import interval_series
import correlations
import isolating_trend
logo = '''

    _____ __        __             __        __                        _
   / ___// /_____ _/ /___  _______/ /___  __/ /______ _   ____  ____  (_)________ _      ______ _
   \__ \/ __/ __ `/ __/ / / / ___/ __/ / / / //_/ __ `/  / __ \/ __ \/ / ___/ __ \ | /| / / __ `/
  ___/ / /_/ /_/ / /_/ /_/ (__  ) /_/ /_/ / ,< / /_/ /  / /_/ / /_/ / (__  ) /_/ / |/ |/ / /_/ /
 /____/\__/\__,_/\__/\__, /____/\__/\__, /_/|_|\__,_/   \____/ .___/_/____/\____/|__/|__/\__,_/  version 1.2
                    /____/         /____/                   /_/                                     
'''


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def go_back(argument='y'):
    print('\nWpisz \'y\' potem nacisnij \'Enter\' jesli chcesz wrocic do menu glownego:', end=' ')
    argument = input()
    funcmap = {'y': main()}
    if (argument == 'y'):
        funcmap['y']


def main():
    cls()
    os.system('mode con: cols=180 lines=40')
    print(logo)
    print('''
    Ktory szereg statystyczny wolisz wybrac? 

      1 - szereg wazony (rozdzielczy punktowy)
      2 - szereg rozdzielczy przedziałowy
      3 - wspolzaleznosc liniowa dwoch cech
      4 - wyodrębniania trendu w szeregach czasowych

    Nacisnij dowolny klawisz aby zamknac.
    ''')
    argument = int(input('    Podaj argument [1, 2 lub 3]: '))
    if (argument == 1):
        cls()
        try:
            point_series.run_point_series()
        except Exception as ex:
            print('\n\t', ex, '---> (Innymi slowy, wystapil blad, zacznij od nowa...)')
            go_back()
        go_back(argument)
    elif (argument == 2):
        cls()
        try:
            interval_series.run_interval_series()
        except Exception as ex:
            print('\n\t', ex, '---> (Innymi slowy, wystapil blad, zacznij od nowa...)')
            go_back()
        go_back(argument)
    elif (argument == 3):
        cls()
        try:
            correlations.run_correlations()
        except Exception as ex:
            print('\n\t', ex, '---> (Innymi slowy, wystapil blad, zacznij od nowa...)')
            go_back()
        go_back(argument)
    elif (argument == 4):
        cls()
        try:
            isolating_trend.run_isolating_trend()
        except Exception as ex:
            print('\n\t', ex, '---> (Innymi slowy, wystapil blad, zacznij od nowa...)')
            go_back()
        go_back(argument)
    else:
        print('nieznany argument, sprobuj ponownie...')
        go_back()
    print('\n')
    os.system("pause")


if __name__ == '__main__':
    main()
