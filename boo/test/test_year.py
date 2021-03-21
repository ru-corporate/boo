import pytest

from boo.year import make_url


def test_make_url_on_0():
    assert make_url(0)


def test_make_url_on_good_year():
    assert make_url(2012)


def test_make_url_on_bad_year():
    with pytest.raises(ValueError):
        make_url(1990)
