## Script

Rosstat published CSV files without column headers. 
When preparing a readable CSV file we assign a name to columns
with variables of interest and cut away the rest of the columns. 

This way we get a much smaller file (~50% of the size). We can read 
and manipulate data from this this file using pandas or R. 

For illustration, batch script below creates `2012.csv` file with column names.

```bat
set url=http://www.gks.ru/opendata/storage/7708234640-bdboo2012/data-20190329t000000-structure-20121231t000000.csv
set  index=1,2,3,4,5,6,7,8,17,18,27,28,37,38,41,42,43,44,57,58,59,60,67,68,69,70,79,80,81,82,83,84,93,94,99,100,105,106,117,118,204,205,209,210,211,212,213,214,215,216,222,223,228,229,235,240,241,266 
set colnames=name,okpo,okopf,okfs,okved,inn,unit,report_type,of,of_lag,ta_fix,ta_fix_lag,cash,cash_lag,ta_nonfix,ta_nonfix_lag,ta,ta_lag,tp_capital,tp_capital_lag,debt_long,debt_long_lag,tp_long,tp_long_lag,debt_short,debt_short_lag,tp_short,tp_short_lag,tp,tp_lag,sales,sales_lag,profit_oper,profit_oper_lag,exp_interest,exp_interest_lag,profit_before_tax,profit_before_tax_lag,profit_after_tax,profit_after_tax_lag,cf_oper_in,cf_oper_in_sales,cf_oper_out,paid_to_supplier,paid_to_worker,paid_interest,paid_profit_tax,paid_other_costs,cf_oper,cf_inv_in,cf_inv_out,paid_fa_investment,cf_inv,cf_fin_in,cf_fin_out,cf_fin,cf,date_published

curl %url% > raw2012.csv

echo %colnames% > 2012.csv
cat raw2012.csv | csvcut -d; -e ansi -c%index%  | iconv -f cp1251 -t utf-8 >> 2012.csv

csvclean 2012.csv
```

Note: this is a Windows batch file, but it relies on GNU utilities (eg via Cygwin, MinGW or [GOW](https://github.com/bmatzelle/gow/wiki)) and [csvkit](https://csvkit.readthedocs.io/en/latest/). Similar script can be adapted for pure linux/bash. [Google colab version](https://colab.research.google.com/drive/1FtwoYfBxzDjGyeQ-BPvcDa6k27DpzuVW) allows a mixin of python and script code, similar to f-strings.

Batch file result is similar to running: 

```python 
from boo import download, build
download(2012)
unpack(2012)
```