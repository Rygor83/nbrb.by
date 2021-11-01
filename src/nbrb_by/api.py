import re
import datetime
import sys
import pandas as pd
import warnings
import nbrb_by.config as config

warnings.simplefilter(action='ignore', category=FutureWarning)


class Api(object):
    """
    API for obtaining: \n
    - the official exchange rate \n
    - the refinancing rate \n
    of the Belarusian ruble against foreign currencies established by the National Bank of the Republic of Belarus
    API helps: \n
    - https://www.nbrb.by/apihelp/exrates \n
    - https://www.nbrb.by/apihelp/refinancingrate \n
    """

    API_BASE_RATE_URL = 'https://www.nbrb.by/API/ExRates/Rates'
    API_BASE_REF_URL = 'https://www.nbrb.by/API/RefinancingRate'
    MIN_YEAR = 1991
    cfg = ""
    url = ""
    orient = ""
    func = 0

    def __init__(self):
        self.cfg = config.Config()

    def get_rates(self, c, d, to=''):
        func = self._get_function(c, d)
        url_dict = self._get_api_rate_url(func, c, d)
        return self._get_json(**url_dict)

    def get_refinance(self, d, all):
        """
        Obtaining info about refinance rate

        :param d: date or no date
        :param all: flag to obtain all rates from the beginning
        :return: data frame with refinance rate info
        """
        url_dict = self._get_api_refinance_url(d, all)
        return self._get_json(**url_dict)

    def _get_function(self, c='', d='', to='') -> int:
        if c is not None and c.upper() == 'BYN':
            # Данные по валюте BYN, которая отстуствует на сайте нац. банка

            func = 9
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

    def _get_api_rate_url(self, func: int, c, d, to='') -> str:
        """
        Method to construct api request url for exchange rates.

        :param self:  self
        :param func: 1 integer id of function
        :param c:    3-letter currency code
        :param d:    date from in needed format
        :param to:   date to in needed format
        :return: url
        """

        if func == 9:
            self.url = 'BYN'
            self.orient = 'index'
        elif func == 1:
            date_from = self._parse_date(d, True)
            date_to = self._parse_date(to, True)
            currency_code = self.cfg.read(c, date_from)
            self.url = self.API_BASE_RATE_URL + f"/Dynamics/{currency_code}?startDate={date_from}&endDate={date_to}"
            self.orient = 'records'
        elif func == 2:
            d = self._parse_date(d, True)
            currency_code = self.cfg.read(c, d)
            # Курс для определеной валюты на дату:
            # https://www.nbrb.by/API/ExRates/Rates/298?onDate=2016-7-5
            self.url = self.API_BASE_RATE_URL + f"/{currency_code}?onDate={d}"
            self.orient = 'index'
        elif func == 3:
            # Курс для определенной валюты сегодня:
            # https://www.nbrb.by/API/ExRates/Rates/USD?ParamMode=2
            self.url = self.API_BASE_RATE_URL + f"/{c}?ParamMode=2"
            self.orient = 'index'
        elif func == 4:
            d = self._parse_date(d, True)
            # Все курсы на определенную дату:
            # https://www.nbrb.by/API/ExRates/Rates?onDate=2016-7-6&Periodicity=0
            self.url = self.API_BASE_RATE_URL + f"?onDate={d}&Periodicity=0"
            self.orient = 'records'
        elif func == 5:
            # Все курсы на сегодня:
            # https://www.nbrb.by/API/ExRates/Rates?Periodicity=0
            self.url = self.API_BASE_RATE_URL + '?Periodicity=0'
            self.orient = 'records'
        else:
            pass

        return {"url": self.url, "orient": self.orient}

    def _get_api_refinance_url(self, d, all):
        """
        Method to construct api request url for refinancing rate.
        :param self:  self
        :param d:    date from in %Y-%m-%d format or no date
        :param all:  flag to obtain all rates
        :return: url
        """
        if d:
            d = self._parse_date(d, True)
            self.url = self.API_BASE_REF_URL + f"?onDate={d}"
        elif all:
            self.url = self.API_BASE_REF_URL
        else:
            today = self._parse_date()
            self.url = self.API_BASE_REF_URL + f"?onDate={today}"

        self.orient = 'records'

        return {"url": self.url, "orient": self.orient}

    def _get_json(self, url, orient):
        if url == 'BYN':
            frame = {"Cur_Abbreviation": "BYN", "Cur_ID": 1, "Cur_Name": "Беларуский рубль", "Cur_OfficialRate": 1,
                     "Cur_Scale": 1, "Date": "2016-07-05T00:00:00"}
            df = pd.DataFrame.from_dict(frame, orient=orient)
        else:
            df = pd.read_json(url, orient)

        return df

    def _parse_date(self, date: str = '', nbrb: bool = '') -> str:
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
            elif length == 0:
                date = datetime.datetime.today().strftime('%Y-%m-%d')
            else:
                print('Не правильная дата')
                input('нажмите Enter ... ')
                sys.exit()

        return date
