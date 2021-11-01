from nbrb_by.config import Config
import pytest
import os


@pytest.fixture
def cfg(tmpdir):
    return Config(tmpdir)


def test_create(tmpdir, cfg):
    cfg.create()
    assert os.path.isfile(cfg.config_path) is True


def test_read_usd_on_01112021(tmpdir, cfg):
    result = cfg.read('usd', '2021-11-01')
    assert 431 == result
