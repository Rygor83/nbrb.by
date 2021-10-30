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
        if os.path.isfile(self.config_path) and os.stat(self.config_path).st_size != 0:
            path = self.config_path
        else:
            print('Не удалось получить нужные параметры т.к. ini файла не существует.')
            print('Для создания запустите команду "ini" и укажите в созданном файле все требуетмые параметры')
            input('нажмите Enter ... ')
            sys.exit()

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
        # parser = ConfigParser()
        # parser['GENERAL'] = {'decimalround': "Round a result up to <decimalround> decimal. Values: integer 1,2,3",
        #                      'copytoclipboard': "Need to copy results into clipboard. Values: True/False",
        #                      'userfriendly': "Need to separate thousands with a space. Values: True/False"}
        #
        # with open(self.config_path, 'w+') as configfile:
        #     parser.write(configfile)
        #
        # click.echo('Path to ini file: %s \n' % click.format_filename(self.config_path))
        # click.echo(click.style('INI file is created'))
        # click.echo(click.style('!!! Fill in all the required parameters in the file !!! \n'))
        # click.launch(self.config_path)
        # click.pause()

        url = 'https://www.nbrb.by/API/ExRates/Currencies'
        orient = 'records'
        json_ini = utilities.retrieve_data_from_url(url, orient)
        json_ini.to_json(self.config_path, 'records')

    def exists(self):
        if os.path.exists(self.config_path):
            return True
        else:
            return False

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


if __name__ == "__main__":
    cfg = Config()
    # cfg.create()

    cur = cfg.read('USD', '2021-10-01')
    print(cur)

    cfg.open_config()
