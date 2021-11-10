"""
Windows Command line for obtaining the official exchange rate and the refinancing rate of the Belarusian ruble
against foreign currencies established by the National Bank of the Republic of Belarus
"""

import click
import pandas as pd
from tabulate import tabulate
from nbrb_by.api import Api


@click.group()
def cli():
    """
    Windows Command line for obtaining the official exchange rate and the refinancing rate of the Belarusian ruble
    against foreign currencies established by the National Bank of the Republic of Belarus
    """


@cli.command('ref')
@click.option('-d', '--date', 'date',
              help='Get a rate on a date. Possible values: 01.01.2021, 01/01/2021, 01-01-2021, 01012021, 010121. '
                   'If empty then today date used.')
@click.option('-all', 'all_dates', is_flag=True, help='Get all Refinance rates', type=click.BOOL)
def ref(date, all_dates):
    """ Refinance rate """
    api = Api()
    refinance_frame = api.get_refinance(date, all_dates)
    refinance_frame['Date'] = pd.to_datetime(refinance_frame['Date']).dt.strftime('%d.%m.%Y')
    refinance_frame = refinance_frame.set_index('Date')
    print(tabulate(refinance_frame, headers='keys', tablefmt='psql'))


@cli.command('conv')
@click.argument('amount')
@click.argument('cur_from')
@click.argument('cur_to')
@click.option('-d', '--date', 'date',
              help='Conversion date. Possible values: 01.01.2021, 01/01/2021, 01-01-2021, 01012021, 010121. '
                   'If empty then today date used.')
def conv(amount, cur_from, cur_to, date=''):
    """
    Currency converter

    Required parameters: \n
    AMOUNT: The amount from which we recalculate, for example: 100 \n
    CUR_FROM: The currency from which we are recalculating, for example: USD \n
    CUR_TO: Currency to be converted into, for example, EUR \n
    Example: nb conv 100 usd eur
    """
    api = Api()

    data_from = api.get_rates(cur_from, date)
    data_to = api.get_rates(cur_to, date)

    amount = float(amount)
    rate_from = float(data_from.loc['Cur_OfficialRate'][0])
    rate_to = float(data_to.loc['Cur_OfficialRate'][0])
    scale_from = float(data_from.loc['Cur_Scale'][0])
    scale_to = float(data_to.loc['Cur_Scale'][0])

    amount_calc = round(amount * (rate_from * scale_to) / (rate_to * scale_from), 2)

    info = [{'Amount from': amount, 'Currency from': str(cur_from).upper(), '=': '=', 'Amount into': amount_calc,
             'Currency into': str(cur_to).upper()}]
    conversion_frame = pd.DataFrame(info)
    conversion_frame = conversion_frame.set_index('Amount from')
    print(tabulate(conversion_frame, headers='keys', tablefmt='psql'))


@cli.command('rate')
@click.argument('currency', required=False)
@click.option('-d', '--date', 'date',
              help='Get a rate on a date. Possible values: 01.01.2021, 01/01/2021, 01-01-2021, 01012021, 010121'
                   'If empty then today date used.')
def rate(currency='', date=''):
    """
    Exchange rates

    Optional argument:
    CURRENCY: Currency for which we want to get the exchange rate. If empty then retrieve all exchange rates.
    """
    info = []

    api = Api()

    df_temp = api.get_rates(currency, date)

    if currency:
        df_temp.loc['Date'] = pd.to_datetime(df_temp.loc['Date']).dt.strftime('%d.%m.%Y')
        info = [
            {'Date': df_temp.loc['Date'][0], f'Rate {str(currency).upper()}': df_temp.loc['Cur_OfficialRate'][0]}]
        exchange_rate_frame = pd.DataFrame(info)
        exchange_rate_frame = exchange_rate_frame.set_index('Date')
    else:
        df_temp['Date'] = pd.to_datetime(df_temp['Date']).dt.strftime('%d.%m.%Y')
        for index, row in df_temp.iterrows():
            info.append(
                {'Currency': row.loc['Cur_Abbreviation'], f"Rate on {row.loc['Date']}": row.loc['Cur_OfficialRate']})
        exchange_rate_frame = pd.DataFrame(info)
        exchange_rate_frame = exchange_rate_frame.set_index('Currency')

    if not currency:  # if currency is not supplied then we retrieve all currency - sort them
        exchange_rate_frame = exchange_rate_frame.sort_values(by=['Currency'], ascending=True)

    print(tabulate(exchange_rate_frame, headers='keys', tablefmt='psql'))


if __name__ == '__main__':
    cli()
