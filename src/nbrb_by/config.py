#  ------------------------------------------
#   Copyright (c) Rygor. 2021.
#  ------------------------------------------
import click
import errno
from appdirs import user_data_dir
import nbrb_by.utilities as utilities
import os
import sys
import datetime
import pandas as pd


class Config():

    def __init__(self):
        self.ini_name = 'nbrb_config.ini'
        self.config_path = os.path.join(self.set_path, self.ini_name)

    def read(self, currency, datum):
        if not os.path.isfile(self.config_path) and os.stat(self.config_path).st_size != 0:
            click.echo("Загружаю справочник валют")
            self.create()

        path = self.config_path

        date_to_compare = datetime.datetime.strptime(datum, '%Y-%m-%d').date()

        currency = str(currency).upper()
        data = pd.read_json(path, orient='records', convert_dates=False)
        data['Cur_DateStart'] = pd.to_datetime(data['Cur_DateStart']).apply(lambda x: x.date())
        data['Cur_DateEnd'] = pd.to_datetime(data['Cur_DateEnd']).apply(lambda x: x.date())

        info = data[(data.Cur_Abbreviation == currency) &
                    (data.Cur_DateStart <= date_to_compare) &
                    (data.Cur_DateEnd >= date_to_compare)]

        if info.empty:
            print(f'Не удалось получить данные по валюте {str(currency).upper()}')
            input('нажмите Enter ... ')
            sys.exit()

        cur_id = info.iloc[0]['Cur_ID']
        return cur_id

    def create(self):
        url = 'https://www.nbrb.by/API/ExRates/Currencies'
        orient = 'records'
        json_ini = utilities.retrieve_data_from_url(url, orient)
        json_ini.to_json(self.config_path, 'records')

    @property
    def set_path(self):
        path = user_data_dir("nbrb_by", appauthor=False)
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        return path

    def open_config(self):
        click.launch(self.config_path)
