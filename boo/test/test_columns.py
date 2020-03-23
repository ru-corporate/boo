from boo.columns import SHORT_COLUMNS, TTL_COLUMNS
from boo.columns import varname_to_code, code_to_varname


def test_varname_to_code_works_for_one_arg():
    assert varname_to_code("ta") == "1600"


def test_code_to_varname_works_for_one_arg():
    assert code_to_varname("4320") == "cf_fin_out"


def test_sc_text():
    assert SHORT_COLUMNS.text == [
        "name",
        "okpo",
        "okopf",
        "okfs",
        "okved",
        "inn",
        "unit",
        "report_type",
        "date_published",
    ]
