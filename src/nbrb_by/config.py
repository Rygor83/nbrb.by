#  ------------------------------------------
#   Copyright (c) Rygor. 2021.
#  ------------------------------------------

""" Configuration file management """

import os
import pathlib
import sys
import datetime
import errno
import click
from appdirs import user_data_dir
import pandas as pd
from typing import Optional


class Config:
    """Configuration file management"""

    def __init__(self, path="", ini_name="") -> None:
        self.path = path if path != "" else user_data_dir("nbrb_by", appauthor=False)
        self.ini_name = ini_name if ini_name != "" else "nbrb_config.ini"
        self.config_path = os.path.join(self.set_path(path=self.path), self.ini_name)

        if not os.path.isfile(self.config_path):
            click.echo("Загружаю справочник валют")
            ret = self.create()
            if ret is None:
                click.echo("List of currencies is reloaded")
            else:
                click.echo(ret)

    def read(self, currency: str, datum: str) -> str:
        """Return currency information object after reading configuration file"""

        date_to_compare = datetime.datetime.strptime(datum, "%Y-%m-%d").date()

        currency = str(currency).upper()
        data = pd.read_json(self.config_path, orient="records", convert_dates=False)
        data["Cur_DateStart"] = pd.to_datetime(data["Cur_DateStart"]).apply(
            lambda x: x.date()
        )
        data["Cur_DateEnd"] = pd.to_datetime(data["Cur_DateEnd"]).apply(
            lambda x: x.date()
        )

        info = data[
            (data.Cur_Abbreviation == currency)
            & (data.Cur_DateStart <= date_to_compare)
            & (data.Cur_DateEnd >= date_to_compare)
            ]

        if info.empty:
            print(f"Не удалось получить данные по валюте {str(currency).upper()}")
            sys.exit()

        cur_id = info.iloc[0]["Cur_ID"]
        return cur_id

    def create(self) -> Optional[str]:
        """Creating a configuration file"""

        url = "https://www.nbrb.by/API/ExRates/Currencies"
        orient = "records"
        json_ini = pd.read_json(url, orient=orient)
        ret = json_ini.to_json(self.config_path, "records")

        return ret

    def set_path(self, path: pathlib.Path) -> pathlib.Path:
        """Setting path for saving config file"""

        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        return path

    def open_config(self) -> None:
        """Open configuration file for editing"""

        click.launch(self.config_path)
