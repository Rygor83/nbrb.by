import pytest
from nbrb_by.api import Api


@pytest.fixture
def api():
    return Api()


dates = {'01.01.2021', '01/01/2021', '01-01-2021', '01012021', '010121'}


# --------------------------------------------------------
# _PARSE_DATE method
# --------------------------------------------------------
@pytest.mark.parametrize("date", dates)
def test_api_parse_all_dates_user_format(api, date):
    d = api._parse_date(date)
    assert d == "01.01.2021"


@pytest.mark.parametrize("date", dates)
def test_api_parse_all_dates_nbrb_format(api, date):
    d = api._parse_date(date, True)
    assert d == "2021-01-01"


# --------------------------------------------------------
# _GET_FUNCTION method
# --------------------------------------------------------

def test_api_get_function_9(api):
    func = api._get_function('BYN')
    assert func == 9


def test_api_get_function_1(api):
    func = api._get_function('USD', date_from='01.01.2021', date_to='31.12.2021')
    assert func == 1


def test_api_get_function_2(api):
    func = api._get_function('EUR', date_from='01.01.2021')
    assert func == 2


def test_api_get_function_3(api):
    func = api._get_function('GBP')
    assert func == 3


def test_api_get_function_4(api):
    func = api._get_function(date_from='01.01.2021')
    assert func == 4


def test_api_get_function_5(api):
    func = api._get_function()
    assert func == 5
