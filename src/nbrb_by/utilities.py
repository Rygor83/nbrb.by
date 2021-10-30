import pandas as pd
import datetime
import re
import sys
from tabulate import tabulate


def retrieve_data_from_url(url, orient):
    data = pd.read_json(url, orient=orient)
    return data


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
        date = re.sub('[-.:/]', '../..', date)
        if nbrb:
            date = datetime.datetime.strptime(date, '%d.%m.%Y').strftime('%Y-%m-%d')
    else:
        length = len(date)
        if length == 6:
            if nbrb:
                date = datetime.datetime.strptime(date, '%d%m%y').strftime('%Y-%m-%d')
            else:
                date = datetime.datetime.strptime(date, '%d%m%y').strftime('%d.%m.%Y')
        elif length == 8:
            if nbrb:
                date = datetime.datetime.strptime(date, '%d%m%Y').strftime('%Y-%m-%d')
            else:
                date = datetime.datetime.strptime(date, '%d%m%Y').strftime('%d.%m.%Y')
        else:
            print('Не правильная дата')
            input('нажмите Enter ... ')
            sys.exit()

    return date


def print_info(data):
    print(tabulate(data, headers='keys', tablefmt='psql'))
