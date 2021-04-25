import os
import point_series
import interval_series
logo = '''

    _____ __        __             __        __                        _
   / ___// /_____ _/ /___  _______/ /___  __/ /______ _   ____  ____  (_)________ _      ______ _
   \__ \/ __/ __ `/ __/ / / / ___/ __/ / / / //_/ __ `/  / __ \/ __ \/ / ___/ __ \ | /| / / __ `/
  ___/ / /_/ /_/ / /_/ /_/ (__  ) /_/ /_/ / ,< / /_/ /  / /_/ / /_/ / (__  ) /_/ / |/ |/ / /_/ /
 /____/\__/\__,_/\__/\__, /____/\__/\__, /_/|_|\__,_/   \____/ .___/_/____/\____/|__/|__/\__,_/   version 1.10
                    /____/         /____/                   /_/                                     
'''


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def go_back(argument):
    print('\nEnter \'y\' if you want to go back')
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

    Nacisnij dowolny klawisz aby zamknac.
    ''')
    argument = int(input('    Podaj argument [1 lub 2]: '))
    if (argument == 1):
        cls()
        point_series.run_point_series()
        go_back(argument)
    elif (argument == 2):
        cls()
        interval_series.run_interval_series()
        go_back(argument)
    else:
        print('nieznany argument, sprobuj ponownie...')
    print('\n')
    os.system("pause")


if __name__ == '__main__':
    main()
