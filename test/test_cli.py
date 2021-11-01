import pytest
from click.testing import CliRunner
from nbrb_by.nbrb_by import ref, conv, rate


# --------------------------------------------------------
# REF command
# --------------------------------------------------------
def test_ref_on_01072021():
    runner = CliRunner()
    result = runner.invoke(ref, "-d 01072021")
    check_value = "        Date  Value\n0 2021-04-21    8.5\n"
    assert result.output == check_value


# --------------------------------------------------------
# RATE command
# --------------------------------------------------------
def test_rate_usd_on_01112021():
    runner = CliRunner()
    result = runner.invoke(rate, "usd -d 01112021")
    check_value = ('                                    0\n'
                   'Cur_ID                            431\n'
                   'Date              2021-11-01T00:00:00\n'
                   'Cur_Abbreviation                  USD\n'
                   'Cur_Scale                           1\n'
                   'Cur_Name                   Доллар США\n'
                   'Cur_OfficialRate               2.4226\n')
    assert result.output == check_value


def test_rate_rub_on_01112021():
    runner = CliRunner()
    result = runner.invoke(rate, "rub -d 01112021")
    check_value = ('                                    0\n'
                   'Cur_ID                            456\n'
                   'Date              2021-11-01T00:00:00\n'
                   'Cur_Abbreviation                  RUB\n'
                   'Cur_Scale                         100\n'
                   'Cur_Name            Российских рублей\n'
                   'Cur_OfficialRate               3.4363\n')
    assert result.output == check_value


# --------------------------------------------------------
# CONV command
# --------------------------------------------------------
def test_conv_1_usd_to_byn_on_01112021():
    runner = CliRunner()
    result = runner.invoke(conv, "1 usd byn -d 01112021")
    check_value = ('   Сумма из Валюта из  =  Сумма в Валюта в\n'
                   '0       1.0       USD  =   2.4226      BYN\n')
    assert result.output == check_value


def test_conv_1_byn_to_usd_on_01112021():
    runner = CliRunner()
    result = runner.invoke(conv, "1 byn usd -d 01112021")
    check_value = ('   Сумма из Валюта из  =  Сумма в Валюта в\n'
                   '0       1.0       BYN  =  0.41278      USD\n')
    assert result.output == check_value


def test_conv_1_byn_to_byn_on_01112021():
    runner = CliRunner()
    result = runner.invoke(conv, "1 byn byn -d 01112021")
    check_value = ('   Сумма из Валюта из  =  Сумма в Валюта в\n'
                   '0       1.0       BYN  =      1.0      BYN\n')
    assert result.output == check_value


@pytest.mark.skip
def test_test():
    pass
