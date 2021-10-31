import re
import datetime
import sys
import pandas as pd

import nbrb_by.config as config


class Api(object):
    API_BASE_URL = 'https://www.nbrb.by/API/ExRates/Rates'
    cfg = ""
    url = ""
    orient = ""

    def __init__(self):
        self.cfg = config.Config()

    def get_function(self, c, d, to=''):
        if c is not None and c.upper() == 'BYN':
            frame = {"Cur_Abbreviation": "BYN", "Cur_ID": 1, "Cur_Name": "Беларуский рубль", "Cur_OfficialRate": 1,
                     "Cur_Scale": 1, "Date": "2016-07-05T00:00:00"}
            data = pd.DataFrame.from_dict(frame, orient='index')

            func = 0
        else:
            if to:
                # Курсы за определенный период:
                # https://www.nbrb.by/API/ExRates/Rates/Dynamics/298?startDate=2016-7-1&endDate=2016-7-30

                func = 1
            elif c and d:
                # Курс для определеной валюты на дату:
                # https://www.nbrb.by/API/ExRates/Rates/298?onDate=2016-7-5

                func = 2
            elif c:
                # Курс для определенной валюты сегодня:
                # https://www.nbrb.by/API/ExRates/Rates/USD?ParamMode=2

                func = 3
            elif d:
                # Все курсы на определенную дату:
                # https://www.nbrb.by/API/ExRates/Rates?onDate=2016-7-6&Periodicity=0

                func = 4
            else:
                # Все курсы на сегодня:
                # https://www.nbrb.by/API/ExRates/Rates?Periodicity=0

                func = 5
            return func

    def get_full_url(self, func: int, c, d, to='') -> str:
        if func == 0:
            pass
        elif func == 1:
            date_from = self.parse_date(d, True)
            date_to = self.parse_date(to, True)
            currency_code = self.cfg.read(c, date_from)
            self.url = self.API_BASE_URL + f"/Dynamics/{currency_code}?startDate={date_from}&endDate={date_to}"
            self.orient = 'records'
        elif func == 2:
            d = self.parse_date(d, True)
            currency_code = self.cfg.read(c, d)
            # Курс для определеной валюты на дату:
            # https://www.nbrb.by/API/ExRates/Rates/298?onDate=2016-7-5
            self.url = self.API_BASE_URL + f"/{currency_code}?onDate={d}"
            self.orient = 'index'
        elif func == 3:
            # Курс для определенной валюты сегодня:
            # https://www.nbrb.by/API/ExRates/Rates/USD?ParamMode=2
            self.url = self.API_BASE_URL + f"/{c}?ParamMode=2"
            self.orient = 'index'
        elif func == 4:
            d = self.parse_date(d, True)
            # Все курсы на определенную дату:
            # https://www.nbrb.by/API/ExRates/Rates?onDate=2016-7-6&Periodicity=0
            self.url = self.API_BASE_URL + f"?onDate={d}&Periodicity=0"
            self.orient = 'records'
        elif func == 5:
            # Все курсы на сегодня:
            # https://www.nbrb.by/API/ExRates/Rates?Periodicity=0
            self.url = self.API_BASE_URL + '?Periodicity=0'
            self.orient = 'records'
        else:
            pass

        return {"url": self.url, "orient": self.orient}

    def get_json(self, url_dict: dict):
        df = pd.read_json(url_dict["url"], orient=url_dict["orient"])
        return df

    def parse_date(self, date: str, nbrb: bool = '') -> str:
        """
        Форматирует полученную на входе дату или для сайта nbrb.by, или же дату в нормальном виде с разделителями точка.
        Допустимый ввод данных: 01.01.19 (допустимый разделитель ./), 01.01.2019, 010119, 01012019
        :param date: Дата
        :param nbrb: True - дата форматируется для сайта nbrb.by, False - обычная дата с разделитерями точно
        :return: дата, в зависимости от параметра nbrb
        """

        delimiters = ['.', '/', '-']

        if any(delimiter in date for delimiter in delimiters):
            date = re.sub('[-.:/]', '.', date)
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
