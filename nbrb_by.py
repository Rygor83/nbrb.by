import click
import configparser
import os
import json
import requests
from prettytable import PrettyTable
import datetime
import sys


def print_sys_table(systems: list):
    header = ['Единица валюты', 'Валюта', '  =  ', 'Курс', 'BYN']
    t = PrettyTable(header)
    for system in systems:
        row = [system[2], system[0], '=', system[1], 'BYN']
        t.add_row(row)
    click.echo(t)


def get_config(currency):
    ini_file = f"{os.path.splitext(os.path.basename(__file__))[0]}.ini"
    if os.path.isfile(ini_file) and os.stat(ini_file).st_size != 0:
        path = os.path.join(os.path.dirname(__file__), ini_file)
    else:
        print('Не удалось получить нужные параметры т.к. ini файла не существует.')
        print('Для создания запустите команду "ini" и укажите в созданном файле все требуетмые параметры')
        sys.exit()

    config = configparser.ConfigParser()
    read = config.read(path)
    if not read:
        print('Не удалось прочитать ini файл')
        sys.exit()
    else:
        return config['CURRENCY'][currency]


def check_existence(file_extension) -> bool:
    if os.path.isfile(f"{os.path.splitext(os.path.basename(__file__))[0]}{file_extension}"):
        file_exists = True
        return file_exists
    else:
        file_exists = False
        return file_exists


def reformat_date(date: str) -> str:
    # Допустимый ввод данных:
    #   01.01.19 (возможный разделитель ./)
    #   01.01.2019
    #   010119
    #   01012019

    if '.' in date:
        delimiter = '.'
        elements = str(date).split(delimiter)
        date = f"{elements[2]}-{elements[1]}-{elements[0]}"
    elif '/' in date:
        delimiter = '/'
        elements = str(date).split(delimiter)
        date = f"{elements[2]}-{elements[1]}-{elements[0]}"
    else:
        length = len(date)
        if length == 6:
            date = f"20{date[4:6]}-{date[2:4]}-{date[0:2]}"
        elif length == 8:
            date = f"{date[4:8]}-{date[2:4]}-{date[0:2]}"
        else:
            pass

    return date


def get_exchange_rate(c, d):
    if c.upper() == 'BYN':
        data = {'Cur_Scale': 1, 'Cur_OfficialRate': 1}
    else:
        base_url = 'http://www.nbrb.by/API/ExRates/Rates'
        if c and d:
            d = reformat_date(d)
            currency_code = get_config(c)
            # Курс для определеной валюты на дату: http://www.nbrb.by/API/ExRates/Rates/298?onDate=2016-7-5
            url = base_url + f"/{currency_code}?onDate={d}"
        elif c:
            # Курс для определенной валюты сегодня: http://www.nbrb.by/API/ExRates/Rates/USD?ParamMode=2
            url = base_url + f"/{c}?ParamMode=2"
        elif d:
            d = reformat_date(d)
            # Все курсы на определенную дату: http://www.nbrb.by/API/ExRates/Rates?onDate=2016-7-6&Periodicity=0
            url = base_url + f"?onDate={d}&Periodicity=0"
        else:
            # Все курсы на сегодня: http://www.nbrb.by/API/ExRates/Rates?Periodicity=0
            url = base_url + '?Periodicity=0'
        response = requests.get(url)
        data = json.loads(response.text)
    return data


@click.group()
def cli():
    """ Скрипт для получения данных с сайта нац. банка РБ """


@cli.command('ini')
def ini():
    """ Создание конфигурационного ini файла """

    file_exists = check_existence('.ini')

    if file_exists:
        print('ini файл уже существует.')
    else:
        config = configparser.ConfigParser()
        response = requests.get('http://www.nbrb.by/API/ExRates/Currencies')
        currencies = json.loads(response.text)

        currency_dictionary = {str(currency['Cur_Abbreviation']).upper(): currency['Cur_ID'] for currency in
                               currencies}
        config['CURRENCY'] = currency_dictionary

        with open(f"{os.path.splitext(os.path.basename(__file__))[0]}.ini", 'w') as configfile:
            config.write(configfile)


@cli.command('cur')
@click.option('-c', help='Валюта')
@click.option('-d', help='Дата запроса')
def cur(c='', d=''):
    """ Курсы валютю """

    # TODO: вывод сообщения, что получили и на какую дату

    data = get_exchange_rate(c, d)
    info = []
    if isinstance(data, list):
        for item in data:
            info.append([item['Cur_Abbreviation'], item['Cur_OfficialRate'], item['Cur_Scale']])
    elif isinstance(data, dict):
        info.append([data['Cur_Abbreviation'], data['Cur_OfficialRate'], data['Cur_Scale']])
    print_sys_table(info)
    input('нажмите Enter ...')


@cli.command('ref')
@click.option('-d', help='дата')
@click.option('-all', is_flag=True)
def ref(d, all):
    """ Ставка рефинансирования """

    base_url = 'http://www.nbrb.by/API/RefinancingRate'

    if d:
        d = reformat_date(d)
        url = base_url + f"?onDate={d}"
    elif all:
        url = base_url
    else:
        today = datetime.datetime.today()
        url = base_url + f"?onDate={today:%Y-%m-%d}"

    response = requests.get(url)
    data = json.loads(response.text)
    for item in data:
        print(item['Date'], ':', item['Value'])
    input('нажмите Enter ...')


@cli.command('calc')
@click.argument('amount')
@click.argument('cur_from')
@click.argument('cur_to')
@click.option('-d', help='Дата')
def calc(amount, cur_from, cur_to, d=''):
    """ Перерасчет валют """

    data_from = get_exchange_rate(cur_from, d)
    data_to = get_exchange_rate(cur_to, d)

    amount_calc = float(amount) * (float(data_from['Cur_OfficialRate']) * float(data_to['Cur_Scale'])) / (
            float(data_to['Cur_OfficialRate']) * float(data_from['Cur_Scale']))
    header = ['Сумма из', 'Валюта из', '  =  ', 'Сумма в', 'Валюта в']
    t = PrettyTable(header)
    row = [amount, str(cur_from).upper(), '=', amount_calc, str(cur_to).upper()]
    t.add_row(row)
    click.echo(t)
    input('нажмите Enter ...')


if __name__ == '__main__':
    cli()
