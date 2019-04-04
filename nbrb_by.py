import click
import configparser
import os
import json
import requests
from prettytable import PrettyTable
import datetime
import sys
import re

ini_file_path = f"{os.path.splitext(os.path.basename(__file__))[0]}.ini"


def print_sys_table(systems: list, text: str):
    header = ['Единица валюты', 'Валюта', '  =  ', 'Курс', 'BYN']
    t = PrettyTable(header)
    t.title = text
    t.align['Единица валюты'] = 'r'
    for system in systems:
        row = [system[2], system[0], '=', system[1], 'BYN']
        t.add_row(row)
    print(t)


def get_config(currency):
    if os.path.isfile(ini_file_path) and os.stat(ini_file_path).st_size != 0:
        path = os.path.join(os.path.dirname(__file__), ini_file_path)
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


def reformat_date(date: str, nbrb: bool = '') -> str:
    """
    Форматирует полученную на входе дату или для сайта nbrb.by, или же дату в нормальном виде с разделителями точка.
    Допустимый ввод данных: 01.01.19 (допустимый разделитель ./), 01.01.2019, 010119, 01012019
    :param date: Дата
    :param nbrb: True - дата форматируется для сайта nbrb.by, False - обычная дата с разделитерями точно
    :return: дата, в зависимости от параметра nbrb
    """

    delimiters = ['.', '/', '-']

    if any(delimiter in date for delimiter in delimiters):
        regex_pattern = '|'.join(map(re.escape, delimiters))
        elements = re.split(regex_pattern, date)  # r"/|\."
        if nbrb:
            date = f"{elements[2]}-{elements[1]}-{elements[0]}"
        else:
            date = f"{elements[0]}.{elements[1]}.{elements[2]}"
    else:
        length = len(date)
        if length == 6:
            if nbrb:
                date = f"20{date[4:6]}-{date[2:4]}-{date[0:2]}"
            else:
                date = f"{date[0:2]}.{date[2:4]}.20{date[4:6]}"
        elif length == 8:
            if nbrb:
                date = f"{date[4:8]}-{date[2:4]}-{date[0:2]}"
            else:
                date = f"{date[0:2]}.{date[2:4]}.{date[4:8]}"
        else:
            print('Не правильная дата')
            input('нажмите Enter ... ')
            sys.exit()

    return date


def get_exchange_rate(c, d):
    if c is not None and c.upper() == 'BYN':
        data = {'Cur_Scale': 1, 'Cur_OfficialRate': 1}
    else:
        base_url = 'http://www.nbrb.by/API/ExRates/Rates'
        if c and d:
            d = reformat_date(d, True)
            currency_code = get_config(c)
            # Курс для определеной валюты на дату: http://www.nbrb.by/API/ExRates/Rates/298?onDate=2016-7-5
            url = base_url + f"/{currency_code}?onDate={d}"
        elif c:
            # Курс для определенной валюты сегодня: http://www.nbrb.by/API/ExRates/Rates/USD?ParamMode=2
            url = base_url + f"/{c}?ParamMode=2"
        elif d:
            d = reformat_date(d, True)
            # Все курсы на определенную дату: http://www.nbrb.by/API/ExRates/Rates?onDate=2016-7-6&Periodicity=0
            url = base_url + f"?onDate={d}&Periodicity=0"
        else:
            # Все курсы на сегодня: http://www.nbrb.by/API/ExRates/Rates?Periodicity=0
            url = base_url + '?Periodicity=0'
        data = retrieve_data_from_url(url)
    return data


def retrieve_data_from_url(url):
    response = requests.get(url)
    data = json.loads(response.text)
    return data


@click.group()
def cli():
    """ Скрипт для получения данных с сайта нац. банка РБ """


@cli.command('ini')
def ini():
    """ Создание конфигурационного ini файла, где сопоставляются ISO коды валют (USD) с внутренними кодами нац. банка"""

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

        with open(ini_file_path, 'w') as configfile:
            config.write(configfile)


@cli.command('kurs')
@click.argument('currency', required=False)
@click.option('-d', help='Дата запроса')
def kurs(currency='', d=''):
    """ Курсы валют """

    # TODO: вывод основных валют ?

    data = get_exchange_rate(currency, d)
    info = []
    if isinstance(data, list):
        for item in data:
            info.append([item['Cur_Abbreviation'], item['Cur_OfficialRate'], item['Cur_Scale']])
    elif isinstance(data, dict):
        info.append([data['Cur_Abbreviation'], data['Cur_OfficialRate'], data['Cur_Scale']])

    if currency and d:
        text = f"Информация для {currency.upper()} на {reformat_date(d)}"
    elif currency:
        text = f"Информация для {currency.upper()} на текущую дату: "
    elif d:
        text = f"Информация для всех валют на {reformat_date(d)}: "
    else:
        text = 'Информация для всех валют на текущую дату'

    print_sys_table(info, text)
    input('нажмите Enter ...')


@cli.command('ref')
@click.option('-d', help='дата')
@click.option('-all', is_flag=True)
def ref(d, all):
    """ Ставка рефинансирования """

    base_url = 'http://www.nbrb.by/API/RefinancingRate'

    if d:
        d = reformat_date(d, True)
        url = base_url + f"?onDate={d}"
    elif all:
        url = base_url
    else:
        today = datetime.datetime.today()
        url = base_url + f"?onDate={today:%Y-%m-%d}"

    data = retrieve_data_from_url(url)

    header = ['Дата', 'Значение']
    t = PrettyTable(header)
    t.title = 'Ставка рефинансирования РБ'

    for item in data:
        elements = str(str(item['Date']).split('T')[0]).split('-')
        date = f"{elements[2]}.{elements[1]}.{elements[0]}"
        row = [date,  item['Value']]
        t.add_row(row)
    print(t)
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

    amount_calc = round(float(amount) * (float(data_from['Cur_OfficialRate']) * float(data_to['Cur_Scale'])) / (
            float(data_to['Cur_OfficialRate']) * float(data_from['Cur_Scale'])), 2)
    header = ['Сумма из', 'Валюта из', '  =  ', 'Сумма в', 'Валюта в']
    t = PrettyTable(header)
    if d:
        t.title = f"Перерасчет на {reformat_date(d)}"
    else:
        t.title = f"Перерасчет на текущую дату"
    row = [amount, str(cur_from).upper(), '=', amount_calc, str(cur_to).upper()]
    t.add_row(row)
    click.echo(t)
    input('нажмите Enter ...')


if __name__ == '__main__':
    cli()
