from nbrb_by.config import Config
import pytest
import os


def test_create(tmpdir):
    cfg = Config(tmpdir)
    cfg.create()
    assert os.path.isfile(cfg.config_path) == True


def test_read_usd_on_01112021(tmpdir):
    cfg = Config(tmpdir)
    result = cfg.read('usd', '2021-11-01')
    assert 431 == result


@pytest.mark.skip
def test_open_config(tmpdir):
    cfg = Config(tmpdir)
    cfg.open_config()
