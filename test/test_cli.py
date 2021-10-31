import pytest
import nbrb_by.api as api


# --------------------------------------------------------
# PARSE_DATE METHOD
# --------------------------------------------------------
def test_api_parse_date_01012021():
    cls = api.Api()
    d = cls.parse_date("01012021")
    assert d == "01.01.2021"


def test_api_parse_date_01012021_true():
    cls = api.Api()
    d = cls.parse_date("01012021", True)
    assert d == "2021-01-01"


def test_api_parse_date_010121():
    cls = api.Api()
    d = cls.parse_date("01012021")
    assert d == "01.01.2021"


def test_api_parse_date_010121_true():
    cls = api.Api()
    d = cls.parse_date("01012021", True)
    assert d == "2021-01-01"


def test_api_parse_date_with_delim_dot():
    cls = api.Api()
    d = cls.parse_date("01.01.2021")
    assert d == "01.01.2021"


def test_api_parse_date_with_delim_dot_true():
    cls = api.Api()
    d = cls.parse_date("01.01.2021", True)
    assert d == "2021-01-01"
