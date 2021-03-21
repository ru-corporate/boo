from boo.columns import INDEX, NAMES, ask, is_lagged


def test_Int64Dtype_falls_to_NA_on_missing_values():
    import io

    import pandas as pd

    source_ = io.StringIO("region,x,y\n77,,20")
    dtype_ = pd.Int64Dtype()
    a = pd.read_csv(source_, dtype=dtype_).to_dict()
    assert pd.isnull(a["x"][0])


def test_same_length():
    assert len(INDEX) == len(NAMES)


def test_is_lagged():
    assert is_lagged("63243") is False
    assert is_lagged("Дата актуализации") is None
    assert is_lagged("23304") is True


def test_ask():
    assert ask("4320") == "cf_fin_out"
