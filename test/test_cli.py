import pytest
from click.testing import CliRunner
from nbrb_by.nbrb_by import ref, conv, rate


@pytest.fixture
def runner():
    return CliRunner()


# --------------------------------------------------------
# REF command
# --------------------------------------------------------
def test_ref_on_01072021(runner):
    result = runner.invoke(ref, "-d 01072021")
    check_value = ('+------------+---------+\n'
                   '| Date       |   Value |\n'
                   '|------------+---------|\n'
                   '| 21.04.2021 |     8.5 |\n'
                   '+------------+---------+\n')
    assert result.output == check_value


# --------------------------------------------------------
# RATE command
# --------------------------------------------------------
def test_rate_usd_on_01112021(runner):
    result = runner.invoke(rate, "usd -d 01112021")
    check_value = ('+------------+------------+\n'
                   '| Date       |   Rate USD |\n'
                   '|------------+------------|\n'
                   '| 01.11.2021 |     2.4226 |\n'
                   '+------------+------------+\n')
    assert result.output == check_value


def test_rate_rub_on_01112021(runner):
    result = runner.invoke(rate, "rub -d 01112021")
    check_value = ('+------------+------------+\n'
                   '| Date       |   Rate RUB |\n'
                   '|------------+------------|\n'
                   '| 01.11.2021 |     3.4363 |\n'
                   '+------------+------------+\n')
    assert result.output == check_value


def test_rate_all_rates_on_01112021(runner):
    result = runner.invoke(rate, "-d 01112021")
    check_value = ('+------------+----------------------+\n'
                   '| Currency   |   Rate on 01.11.2021 |\n'
                   '|------------+----------------------|\n'
                   '| AUD        |               1.826  |\n'
                   '| AMD        |               5.0735 |\n'
                   '| BGN        |               1.4434 |\n'
                   '| UAH        |               9.2263 |\n'
                   '| DKK        |               3.7949 |\n'
                   '| USD        |               2.4226 |\n'
                   '| EUR        |               2.8233 |\n'
                   '| PLN        |               6.114  |\n'
                   '| JPY        |               2.1304 |\n'
                   '| IRR        |               5.7681 |\n'
                   '| ISK        |               1.8845 |\n'
                   '| CAD        |               1.9631 |\n'
                   '| CNY        |               3.7873 |\n'
                   '| KWD        |               8.0333 |\n'
                   '| MDL        |               1.3891 |\n'
                   '| NZD        |               1.7389 |\n'
                   '| NOK        |               2.9009 |\n'
                   '| RUB        |               3.4363 |\n'
                   '| XDR        |               3.4243 |\n'
                   '| SGD        |               1.8006 |\n'
                   '| KGS        |               2.856  |\n'
                   '| KZT        |               5.6623 |\n'
                   '| TRY        |               2.5234 |\n'
                   '| GBP        |               3.3412 |\n'
                   '| CZK        |              10.9968 |\n'
                   '| SEK        |               2.8378 |\n'
                   '| CHF        |               2.659  |\n'
                   '+------------+----------------------+\n')
    assert result.output == check_value


# --------------------------------------------------------
# CONV command
# --------------------------------------------------------
def test_conv_1_usd_to_byn_on_01112021(runner):
    result = runner.invoke(conv, "1 usd byn -d 01112021")
    check_value = ('+---------------+-----------------+-----+---------------+-----------------+\n'
                   '|   Amount from | Currency from   | =   |   Amount into | Currency into   |\n'
                   '|---------------+-----------------+-----+---------------+-----------------|\n'
                   '|             1 | USD             | =   |        2.4226 | BYN             |\n'
                   '+---------------+-----------------+-----+---------------+-----------------+\n')
    assert result.output == check_value


def test_conv_1_byn_to_usd_on_01112021(runner):
    result = runner.invoke(conv, "1 byn usd -d 01112021")
    check_value = ('+---------------+-----------------+-----+---------------+-----------------+\n'
                   '|   Amount from | Currency from   | =   |   Amount into | Currency into   |\n'
                   '|---------------+-----------------+-----+---------------+-----------------|\n'
                   '|             1 | BYN             | =   |       0.41278 | USD             |\n'
                   '+---------------+-----------------+-----+---------------+-----------------+\n')
    assert result.output == check_value


def test_conv_1_byn_to_byn_on_01112021(runner):
    result = runner.invoke(conv, "1 byn byn -d 01112021")
    check_value = ('+---------------+-----------------+-----+---------------+-----------------+\n'
                   '|   Amount from | Currency from   | =   |   Amount into | Currency into   |\n'
                   '|---------------+-----------------+-----+---------------+-----------------|\n'
                   '|             1 | BYN             | =   |             1 | BYN             |\n'
                   '+---------------+-----------------+-----+---------------+-----------------+\n')
    assert result.output == check_value
