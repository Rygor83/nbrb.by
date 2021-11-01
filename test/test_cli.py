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
