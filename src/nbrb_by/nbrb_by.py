import click
import pandas as pd
from nbrb_by.api import Api


@click.group()
def cli():
    """
    Windows Command line for obtaining the official exchange rate and the refinancing rate of the Belarusian ruble
    against foreign currencies established by the National Bank of the Republic of Belarus
    """


@cli.command('ref')
@click.option('-d', '--date', 'date',
              help='Get a rate on a date. Possible values: 01.01.2021, 01/01/2021, 01-01-2021, 01012021, 010121')
@click.option('-all', is_flag=True, help='Get all Refinance rates', type=click.BOOL)
def ref(date, all):
    """ Refinance rate """
    api = Api()
    dt = api.get_refinance(date, all)
    print(dt)


@cli.command('conv')
@click.argument('amount')
@click.argument('cur_from')
@click.argument('cur_to')
@click.option('-d', '--date', 'date',
              help='Recalculation date. Possible values: 01.01.2021, 01/01/2021, 01-01-2021, 01012021, 010121')
def conv(amount, cur_from, cur_to, date=''):
    """
    Exchange rates \n
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

    amount_calc = amount * (rate_from * scale_to) / (rate_to * scale_from)

    info = [{'Сумма из': amount, 'Валюта из': str(cur_from).upper(), '=': '=', 'Сумма в': amount_calc,
             'Валюта в': str(cur_to).upper()}]
    data = pd.DataFrame(info)
    data.set_index('Сумма из')
    print(data)


@cli.command('rate')
@click.argument('currency', required=False)
@click.option('-d', help='Get a rate on a date. Possible values: 01.01.2021, 01/01/2021, 01-01-2021, 01012021, 010121')
def rate(currency='', d=''):
    """
    Currency converter

    Optional parameter:
    CURRENCY: Currency for which we want to get the exchange rate.
    """

    api = Api()

    dt = api.get_rates(currency, d)
    print(dt)


if __name__ == '__main__':
    cli()
