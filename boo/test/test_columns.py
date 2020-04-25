from boo.columns import INDEX, NAMES
from boo.columns import ask
from boo.columns import is_lagged


def test_smae_length():
    assert len(INDEX) == len(NAMES)


def test_is_lagged():
    assert is_lagged("63243") is False
    assert is_lagged("Дата актуализации") is None
    assert is_lagged("23304") is True


def test_ask():
    assert ask("4320") == "cf_fin_out"
