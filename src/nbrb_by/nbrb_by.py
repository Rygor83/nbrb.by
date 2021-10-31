import click
from nbrb_by import api as api


@click.group()
def cli():
    """ Скрипт для получения данных с сайта нац. банка РБ """


# @cli.command('ref')
# @click.option('-d', help='Получить ставку на указанную дату')
# @click.option('-all', is_flag=True, help='Показать динамику изменений ставки')
# @click.option('-g', is_flag=True, help='Отрисовать график колебания курсов')
# def ref(d, all, g):
#     """ Ставка рефинансирования """
#
#     base_url = 'https://www.nbrb.by/API/RefinancingRate'
#
#     if d:
#         d = utilities.reformat_date(d, True)
#         url = base_url + f"?onDate={d}"
#     elif all:
#         url = base_url
#     else:
#         today = datetime.datetime.today()
#         url = base_url + f"?onDate={today:%Y-%m-%d}"
#
#     orient = 'records'
#     data = utilities.retrieve_data_from_url(url, orient)
#     data['Date'] = pd.to_datetime(data['Date']).dt.strftime('%d.%m.%Y')
#     data.columns = ['Дата', 'Ставка Реф.']
#     utilities.print_info(data)


# @cli.command('conv')
# @click.argument('amount')
# @click.argument('cur_from')
# @click.argument('cur_to')
# @click.option('-d', help='Дата')
# def conv(amount, cur_from, cur_to, d=''):
#     """
#     Перерасчет валют \n
#     Обязательные параметры: \n
#     amount: Сумма, из которой делаем перерасчет, например: 100 \n
#     cur_from: Валюта, из которой делаем перерасчет, например: USD \n
#     cur_to: Валюта, в которую нужно сделать перерасчет, например, EUR \n
#     Пример командной строки: 100 usd eur
#     """
#
#     # TODO: добавить флаг -all, чтобы перерасчитывать исходную валюту во все (возможно основные).
#
#     data_from = get_exchange_rate(cur_from, d)
#     data_to = get_exchange_rate(cur_to, d)
#
#     amount = float(amount)
#     rate_from = float(data_from.loc['Cur_OfficialRate'][0])
#     rate_to = float(data_to.loc['Cur_OfficialRate'][0])
#     scale_from = float(data_from.loc['Cur_Scale'][0])
#     scale_to = float(data_to.loc['Cur_Scale'][0])
#
#     amount_calc = amount * (rate_from * scale_to) / (rate_to * scale_from)
#
#     info = [{'Сумма из': amount, 'Валюта из': str(cur_from).upper(), '=': '=', 'Сумма в': amount_calc,
#              'Валюта в': str(cur_to).upper()}]
#     data = pd.DataFrame(info)
#     data.set_index('Сумма из')
#     utilities.print_info(data)


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

    if all:
        pass
        # date_from = input('Введите дату "С": ')
        # date_to = input('Введите дату "По": ')
        # # https://www.nbrb.by/API/ExRates/Rates/Dynamics/298?startDate=2016-7-1&endDate=2016-7-30
        # rate_info = get_exchange_rate(currency, date_from, date_to)
        # rate_info['Date'] = pd.to_datetime(rate_info['Date']).dt.strftime('%d.%m.%Y')
        # data = rate_info.loc[:, 'Date':'Cur_OfficialRate']
        # data.columns = ['Дата', f'Курс {str(currency).upper()}']
    else:
        rate_obj = api.Api()
        func = rate_obj.get_function(currency, d)
        url_dict = rate_obj.get_full_url(func, currency, d)
        js = rate_obj.get_json(url_dict)
        print(js)

        # print(tabulate(js, headers='keys', tablefmt='psql'))

    #     rate_info = get_exchange_rate(currency, d)
    #     rate_info.loc['Date'] = pd.to_datetime(rate_info.loc['Date']).dt.strftime('%d.%m.%Y')
    #     info = [
    #         {'Дата': rate_info.loc['Date'][0], f'Курс {str(currency).upper()}': rate_info.loc['Cur_OfficialRate'][0]}]
    #     data = pd.DataFrame(info)
    #
    # utilities.print_info(data)


if __name__ == '__main__':
    cli()
