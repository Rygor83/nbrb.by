"""
Windows/Linux Command line for obtaining the official exchange rate and the refinancing rate of the Belarusian ruble
against foreign currencies established by the National Bank of the Republic of Belarus
"""

import click
import pandas as pd
from tabulate import tabulate
import pyperclip
from nbrb_by.api import Api
from nbrb_by.config import Config

# TODO: Сделать возможность переходить на сайт нац.банка

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def open_site_ref(ctx, param, value):
    """
    Open configuration file for editing
    """
    if not value or ctx.resilient_parsing:
        return

    click.launch(url="https://www.nbrb.by/statistics/monetarypolicyinstruments/refinancingrate")

    ctx.exit()


def open_site_rate(ctx, param, value):
    """
    Open configuration file for editing
    """
    if not value or ctx.resilient_parsing:
        return

    click.launch(url="https://www.nbrb.by/statistics/rates/ratesdaily.asp")

    ctx.exit()


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """
    Windows Command line for obtaining the official exchange rate and the refinancing rate of the Belarusian ruble
    against foreign currencies established by the National Bank of the Republic of Belarus
    """


@cli.command("ref")
@click.option(
    "-d",
    "--date",
    "date",
    help="Get a rate on a date. Possible values: 01.01.2021, 01/01/2021, 01-01-2021, 01012021, 010121. "
         "If empty then today date used.",
)
@click.option(
    "-all", "all_dates", is_flag=True, help="Get all Refinance rates", type=click.BOOL
)
@click.option('-w', is_flag=True, callback=open_site_ref, expose_value=False,
              is_eager=True,
              help='Open national bank website with information about refinance rates')
def ref(date: str, all_dates: bool) -> None:
    """Refinance rate"""
    api = Api()
    refinance_frame = api.get_refinance(date, all_dates)
    pyperclip.copy(refinance_frame.loc[0].Value)
    refinance_frame["Date"] = pd.to_datetime(refinance_frame["Date"]).dt.strftime(
        "%d.%m.%Y"
    )
    refinance_frame = refinance_frame.set_index("Date")
    print(tabulate(refinance_frame, headers="keys", tablefmt="psql"))


@cli.command("conv")
@click.argument("amount")
@click.argument("cur_from")
@click.argument("cur_to")
@click.option(
    "-d",
    "--date",
    "date",
    help="Conversion date. Possible values: 01.01.2021, 01/01/2021, 01-01-2021, 01012021, 010121. "
         "If empty then today date used.",
)
def conv(amount: float, cur_from: str, cur_to: str, date: str = "") -> None:
    """
    \b
    Currency converter
    \b
    Required parameters:
    AMOUNT: The amount from which we recalculate, for example: 100
    CUR_FROM: The currency from which we are recalculating, for example: USD
    CUR_TO: Currency to be converted into, for example, EUR
    Example: nb conv 100 usd eur
    """
    api = Api()

    data_from = api.get_rates(cur_from, date)
    data_to = api.get_rates(cur_to, date)

    amount = float(amount)
    rate_from = float(data_from.loc["Cur_OfficialRate"][0])
    rate_to = float(data_to.loc["Cur_OfficialRate"][0])
    scale_from = float(data_from.loc["Cur_Scale"][0])
    scale_to = float(data_to.loc["Cur_Scale"][0])

    amount_calc = round(amount * (rate_from * scale_to) / (rate_to * scale_from), 2)

    pyperclip.copy(amount_calc)

    info = [
        {
            "Amount from": amount,
            "Currency from": str(cur_from).upper(),
            "=": "=",
            "Amount into": amount_calc,
            "Currency into": str(cur_to).upper(),
        }
    ]
    conversion_frame = pd.DataFrame(info)
    conversion_frame = conversion_frame.set_index("Amount from")
    print(tabulate(conversion_frame, headers="keys", tablefmt="psql"))


@cli.command("rate")
@click.argument("currency", required=False)
@click.option(
    "-d",
    "--date",
    "date",
    help="Get a rate on a date. Possible values: 01.01.2021, 01/01/2021, 01-01-2021, 01012021, 010121"
         "If empty then today date used.",
)
@click.option(
    '-w', is_flag=True, callback=open_site_rate, expose_value=False,
    is_eager=True,
    help='Open national bank website with information about exchange rates'
)
def rate(currency: str = "", date: str = "") -> None:
    """
    \b
    Exchange rates
    \b
    Optional argument:
    CURRENCY: Currency for which we want to get the exchange rate.
    \b
    If empty then retrieve all exchange rates.
    """
    info = []

    api = Api()

    df_temp = api.get_rates(currency, date)

    if currency:
        df_temp.loc["Date"] = pd.to_datetime(df_temp.loc["Date"]).dt.strftime(
            "%d.%m.%Y"
        )
        pyperclip.copy(df_temp.loc["Cur_OfficialRate"][0])
        info = [
            {
                "Date": df_temp.loc["Date"][0],
                f"Rate {str(currency).upper()}": df_temp.loc["Cur_OfficialRate"][0],
            }
        ]
        exchange_rate_frame = pd.DataFrame(info)
        exchange_rate_frame = exchange_rate_frame.set_index("Date")
    else:
        df_temp["Date"] = pd.to_datetime(df_temp["Date"]).dt.strftime("%d.%m.%Y")
        for index, row in df_temp.iterrows():
            info.append(
                {
                    "Currency": row.loc["Cur_Abbreviation"],
                    f"Rate on {row.loc['Date']}": row.loc["Cur_OfficialRate"],
                }
            )
        exchange_rate_frame = pd.DataFrame(info)
        exchange_rate_frame = exchange_rate_frame.set_index("Currency")

    if (
            not currency
    ):  # if currency is not supplied then we retrieve all currency - sort them
        exchange_rate_frame = exchange_rate_frame.sort_values(
            by=["Currency"], ascending=True
        )

    print(tabulate(exchange_rate_frame, headers="keys", tablefmt="psql"))


@cli.command("config")
@click.option(
    "-reload",
    "reload_config",
    type=click.BOOL,
    is_flag=True,
    help="Reload list of currencies",
)
@click.option(
    "-open",
    "open_config",
    type=click.BOOL,
    is_flag=True,
    help="Open config",
)
def config(reload_config: bool, open_config: bool) -> None:
    """
    \b
    Operations with config
    \b
    1. Reload from nbrb.by list of currencies and their parameters
    2. Open config
    """
    cfg = Config()
    if reload_config:
        ret = cfg.create()
        if ret is None:
            click.echo("List of currencies is reloaded")
        else:
            click.echo(ret)
    elif open_config:
        cfg.open_config()
    else:
        click.echo("Enter subcommand: -reload or -open")


if __name__ == "__main__":
    cli()
