import pytest

from tempfile import TemporaryDirectory
from requests.exceptions import ConnectionError
from boo.downloader import csv_filename, mk_url, download, unpack
from boo.reader import read_dataframe


def test_csv_filename():
    assert csv_filename(2012) == "data-20200331-structure-20121231.csv"

def test_mk_url():
    assert (mk_url(2018)
    == "https://rosstat.gov.ru/opendata/7708234640-7708234640bdboo2018/data-20200327-structure-20181231.zip"
)    

def test_make_url_on_0():
    assert mk_url(0)


def test_make_url_on_bad_year():
    with pytest.raises(KeyError):
        mk_url(1990)


def test_download_unpack_read():
    try:
        with TemporaryDirectory() as temp_dir:
            download(year=0, directory=str(temp_dir))
            unpack(year=0, directory=str(temp_dir))
            df = read_dataframe(year=0, directory=str(temp_dir))
            assert df.index.to_list() == ['2457009983',
 '3328100636',
 '3125008321',
 '2312128916',
 '2309001660',
 '2446000322',
 '4200000333',
 '2703005461',
 '2312031047',
 '2420002597']
            assert df.iloc[:1,:].to_csv(line_terminator="\r\n") == reference_csv()
    # test passes if no internet connection available
    except ConnectionError:
        pass

def reference_csv():
    return 'inn,title,org,okpo,okopf,okfs,okved,unit,ok1,ok2,ok3,region,of,of_lag,ta_fix_fin,ta_fix_fin_lag,ta_fix,ta_fix_lag,inventory,inventory_lag,receivables,receivables_lag,ta_nonfix_fin,ta_nonfix_fin_lag,cash,cash_lag,ta_nonfix,ta_nonfix_lag,ta,ta_lag,retained_earnings,retained_earnings_lag,tp_capital,tp_capital_lag,debt_long,debt_long_lag,tp_long,tp_long_lag,debt_short,debt_short_lag,payables,payables_lag,tp_short,tp_short_lag,tp,tp_lag,sales,sales_lag,costs,costs_lag,profit_oper,profit_oper_lag,exp_interest,exp_interest_lag,profit_before_tax,profit_before_tax_lag,profit_after_tax,profit_after_tax_lag,cf_oper_in,cf_oper_in_sales,cf_oper_out,paid_to_supplier,paid_to_worker,paid_interest,paid_profit_tax,cf_oper,cf_inv_in,cf_inv_out,paid_fa_investment,cf_inv,cf_fin_in,cf_loan_in,cf_eq_in_1,cf_eq_in_2,cf_bond_in,cf_fin_out,cf_eq_out,cf_div_out,cf_debt_out,cf_fin,cf\r\n2457009983,"Российское акционерное общество по производству цветных и драгоценных металлов ""Норильский никель""",Открытое акционерное общество,00002565,47,16,65.23.1,384,65,23,1,24,56,91,3129154,3129154,3147918,3145711,23,37,1951,4704,2900387,2770211,13763,20799,2916124,2795751,6064042,5941462,7087,7087,6062376,5939884,0,0,0,0,0,0,360,288,1666,1578,6064042,5941462,2951506,2846978,2770211,2650203,128356,145699,0,0,147354,142071,122492,112870,2952890,0,2989704,15215,32857,0,27105,-36814,29792,0,0,29792,0,0,0,0,0,0,0,0,0,0,-7022\r\n'
