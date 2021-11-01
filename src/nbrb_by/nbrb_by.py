import click
import pandas as pd
import tabulate
from nbrb_by.api import Api


@click.group()
def cli():
    """ Скрипт для получения данных с сайта нац. банка РБ """


@cli.command('ref')
@click.option('-d', help='Получить ставку на указанную дату')
@click.option('-all', is_flag=True, help='Показать динамику изменений ставки')
def ref(d, all):
    """ Ставка рефинансирования """
    api = Api()
    js = api.get_refinance(d, all)
    print(js)


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
    api = Api()

    data_from = api.get_rates(cur_from, d)
    data_to = api.get_rates(cur_to, d)

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
@click.option('-d', help='Дата, на которую хотим получить курс. Используется совместо с указаниева валюты,\
 для которой хотим получить курс')
@click.option('-all', is_flag=True, help='Получить курсы за перид')
@click.option('-g', is_flag=True, help='Отрисовать график колебания курсов')
def rate(currency='', d='', all='', g=''):
    """
    Курсы валют

    Опционный параметр:
    currency: Валюта, для которой хотим получить курс.
    """

    api = Api()

    js = api.get_rates(currency, d)
    print(js)


if __name__ == '__main__':
    cli()
