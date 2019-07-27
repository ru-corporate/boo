from boo.whatis import whatis


def test_whatis_returns_name():
    assert whatis("cash") == 'Денежные средства и денежные эквиваленты'

def test_whatis_returns_additional_name():
    assert whatis("ok1") == 'Код ОКВЭД первого уровня'

def test_whatis_returns_on_shorthand():
    assert whatis('p') == "Прибыль (убыток) до налогообложения"
    
def test_whatis_is_confused():
    assert whatis("aha!") is None
