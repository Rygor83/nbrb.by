import pandas as pd
import datetime
import re
import sys
from tabulate import tabulate


def retrieve_data_from_url(url, orient):
    data = pd.read_json(url, orient=orient)
    return data





def print_info(data):
    print(tabulate(data, headers='keys', tablefmt='psql'))
