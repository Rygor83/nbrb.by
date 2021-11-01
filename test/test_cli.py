import pytest
from nbrb_by.api import Api


# --------------------------------------------------------
# _PARSE_DATE method
# --------------------------------------------------------
def test_api_parse_date_01012021():
    api = Api()
    d = api._parse_date("01012021")
    assert d == "01.01.2021"


def test_api_parse_date_01012021_true():
    api = Api()
    d = api._parse_date("01012021", True)
    assert d == "2021-01-01"


def test_api_parse_date_010121():
    api = Api()
    d = api._parse_date("01012021")
    assert d == "01.01.2021"


def test_api_parse_date_010121_true():
    api = Api()
    d = api._parse_date("01012021", True)
    assert d == "2021-01-01"


def test_api_parse_date_with_delim_dot():
    api = Api()
    d = api._parse_date("01.01.2021")
    assert d == "01.01.2021"


def test_api_parse_date_with_delim_dot_true():
    api = Api()
    d = api._parse_date("01.01.2021", True)
    assert d == "2021-01-01"


# --------------------------------------------------------
# _GET_FUNCTION method
# --------------------------------------------------------

def test_api_get_function_9():
    api = Api()
    func = api._get_function('BYN')
    assert func == 9


def test_api_get_function_1():
    api = Api()
    func = api._get_function('USD', d='01.01.2021', to='31.12.2021')
    assert func == 1


def test_api_get_function_2():
    api = Api()
    func = api._get_function('EUR', d='01.01.2021')
    assert func == 2


def test_api_get_function_3():
    api = Api()
    func = api._get_function('GBP')
    assert func == 3


def test_api_get_function_4():
    api = Api()
    func = api._get_function(d='01.01.2021')
    assert func == 4


def test_api_get_function_5():
    api = Api()
    func = api._get_function()
    assert func == 5
