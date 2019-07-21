from boo.whatis import whatis


def test_whatis_returns_name():
    assert whatis("cash") == 'Денежные средства и денежные эквиваленты'


def test_whatis_is_confused():
    assert whatis("aha!") is None
