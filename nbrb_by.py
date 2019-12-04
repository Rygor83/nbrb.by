import datetime
import os
import re
import sys
import click
import pandas as pd
from prettytable import PrettyTable
from tabulate import tabulate

ini_file_path = f"{os.path.splitext(os.path.basename(__file__))[0]}.ini"

# TODO: сделать флаг, чтобы вместо таблицы выводить график. Возможно динамический, чтобы можно было найти для курса - дату и наоборот.

def print_sys_table(systems: list, text: str):
    if len(systems[0]) == 3:
        header = ['Единица валюты', 'Валюта', '  =  ', 'Курс', 'BYN']
        t = PrettyTable(header)
        t.title = text
        t.align['Единица валюты'] = 'r'
        for system in systems:
            row = [system[2], system[0], '=', system[1], 'BYN']
            t.add_row(row)
    elif len(systems[0]) == 2:
        header = ['Дата', 'Курс']
        t = PrettyTable(header)
        t.title = text
        t.align['Курс'] = 'l'
        for system in systems:
            row = [system[0], system[1]]
            t.add_row(row)
    print(t)


def get_config(currency, datum):
    if os.path.isfile(ini_file_path) and os.stat(ini_file_path).st_size != 0:
        path = os.path.join(os.path.dirname(__file__), ini_file_path)
    else:
        print('Не удалось получить нужные параметры т.к. ini файла не существует.')
        print('Для создания запустите команду "ini" и укажите в созданном файле все требуетмые параметры')
        sys.exit()

    date_to_compare = datetime.datetime.strptime(datum, '%Y-%m-%d').date()

    currency = str(currency).upper()
    data = pd.read_json(path, orient='records', convert_dates=False)
    data['Cur_DateStart'] = pd.to_datetime(data['Cur_DateStart']).apply(lambda x: x.date())
    data['Cur_DateEnd'] = pd.to_datetime(data['Cur_DateEnd']).apply(lambda x: x.date())

    info = data[(data.Cur_Abbreviation == currency) &
                (data.Cur_DateStart <= date_to_compare) &
                (data.Cur_DateEnd >= date_to_compare)]

    cur_id = info.iloc[0]['Cur_ID']
    return cur_id


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


def get_exchange_rate(c, d, to=''):
    if c is not None and c.upper() == 'BYN':
        data = {'Cur_Scale': 1, 'Cur_OfficialRate': 1}
    else:
        base_url = 'http://www.nbrb.by/API/ExRates/Rates'
        if to:
            # Курсы за определенный период:
            # http://www.nbrb.by/API/ExRates/Rates/Dynamics/298?startDate=2016-7-1&endDate=2016-7-30
            date_from = reformat_date(d, True)
            date_to = reformat_date(to, True)
            currency_code = get_config(c, date_from)
            url = base_url + f"/Dynamics/{currency_code}?startDate={date_from}&endDate={date_to}"
            orient = 'records'
        elif c and d:
            d = reformat_date(d, True)
            currency_code = get_config(c, d)
            # Курс для определеной валюты на дату:
            # http://www.nbrb.by/API/ExRates/Rates/298?onDate=2016-7-5
            url = base_url + f"/{currency_code}?onDate={d}"
            orient = 'index'
        elif c:
            # Курс для определенной валюты сегодня:
            # http://www.nbrb.by/API/ExRates/Rates/USD?ParamMode=2
            url = base_url + f"/{c}?ParamMode=2"
            orient = 'index'
        elif d:
            d = reformat_date(d, True)
            # Все курсы на определенную дату:
            # http://www.nbrb.by/API/ExRates/Rates?onDate=2016-7-6&Periodicity=0
            url = base_url + f"?onDate={d}&Periodicity=0"
            orient = 'records'
        else:
            # Все курсы на сегодня:
            # http://www.nbrb.by/API/ExRates/Rates?Periodicity=0
            url = base_url + '?Periodicity=0'
            orient = 'records'

        data = retrieve_data_from_url(url, orient)
    return data


def retrieve_data_from_url(url, orient):
    data = pd.read_json(url, orient=orient)
    return data


@click.group()
def cli():
    """ Скрипт для получения данных с сайта нац. банка РБ """


@cli.command('ini')
def ini():
    """ Создание конфигурационного ini файла, где сопоставляются ISO коды валют (USD) с внутренними кодами нац. банка"""

    url = 'http://www.nbrb.by/API/ExRates/Currencies'
    orient = 'records'
    json_ini = retrieve_data_from_url(url, orient)
    json_ini.to_json(ini_file_path, 'records')


@cli.command('rate')
@click.argument('currency', required=False)
@click.option('-d', help='Дата, на которую хотим получить курс. Используется совместо с указаниева валюты,\
 для которой хотим получить курс')
@click.option('-all', is_flag=True, help='Получить курсы на текущую дату для всех валют')
def rate(currency='', d='', all=''):
    """
    Курсы валют

    Опционный параметр:
    currency: Валюта, для которой хотим получить курс.
    """

    #TODO: выводить график движенния курса при запросе

    if all:
        date_from = input('Введите дату "С": ')
        date_to = input('Введите дату "По": ')
        # http://www.nbrb.by/API/ExRates/Rates/Dynamics/298?startDate=2016-7-1&endDate=2016-7-30
        data = get_exchange_rate(currency, date_from, date_to)
    else:
        data = get_exchange_rate(currency, d)

    print(tabulate(data, headers='keys', tablefmt='psql'))
    input('нажмите Enter ...')


@cli.command('ref')
@click.option('-d', help='Получить ставку на указанную дату')
@click.option('-all', is_flag=True, help='Показать динамику изменений ставки')
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

    orient = 'records'
    data = retrieve_data_from_url(url, orient)

    print(tabulate(data, headers='keys', tablefmt='psql'))
    input('нажмите Enter ...')


@cli.command('conv')
@click.argument('amount')
@click.argument('cur_from')
@click.argument('cur_to')
@click.option('-d', help='Дата')
def conv(amount, cur_from, cur_to, d=''):
    """
    Перерасчет валют \n
    Обязательные параметры: \n
    amount: Сумма, из которой делаем перерасчет, например: 100 \n
    cur_from: Валюта, из которой делаем перерасчет, например: USD \n
    cur_to: Валюта, в которую нужно сделать перерасчет, например, EUR \n
    Пример командной строки: 100 usd eur
    """

    # TODO: добавить флаг -all, чтобы перерасчитывать исходную валюту во все (возможно основные).
    data_from = get_exchange_rate(cur_from, d)
    data_to = get_exchange_rate(cur_to, d)

    amount = float(amount)
    cur_from = float(data_from.loc['Cur_OfficialRate'][0])
    cur_to = float(data_to.loc['Cur_OfficialRate'][0])
    scale_from = float(data_from.loc['Cur_Scale'][0])
    scale_to = float(data_to.loc['Cur_Scale'][0])

    amount_calc = amount * (cur_from * scale_to) / (cur_to * scale_from)

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
