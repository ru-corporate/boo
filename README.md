[![PyPI](https://img.shields.io/pypi/v/boo.svg)](https://pypi.python.org/pypi/boo/#history)
[![Build Status](https://travis-ci.com/ru-corporate/boo.svg?branch=master)](https://travis-ci.com/ru-corporate/boo)
[![Coverage Status](https://coveralls.io/repos/github/ru-corporate/boo/badge.svg?branch=master&service=github)](https://coveralls.io/github/ru-corporate/boo?branch=master)
[![colab](https://img.shields.io/badge/colab-launch-blue.svg)](https://colab.research.google.com/drive/11g70BD78BnM6PqVrT4uZ27zrNBQ2ae3s#scrollTo=YD-la400CQyT)

# boo

`boo` is a Python client to download and transform annual corporate report data from Rosstat website. 
`boo` creates a local CSV file with column names, importable as pandas dataframe. 

## Install

```
pip install boo
```

For development version:

```
pip install git+https://github.com/ru-corporate/boo.git@master
```

## Usage

```python
from boo import download, build, read_dataframe

download(2012)
build(2012)
df = read_dataframe(2012)
print(df.head())
```

## Files
 
CSV files are located at `~/.boo` folder. `boo.locate(year)` will show exactly where they are.

File name     | Description  | Column count |  Created by 
--------------|--------------|:------------:|:------------:
`raw<year>.csv`     | Original CSV file from Rosstat website. No header row.    | 266 | `download(year)`
`<year>.csv` | CSV file with column names in header row.  | 58 | `build(year)`

`df = read_dataframe(year)` returns reference ("canonic") dataset. This function makes 
additional column transformations (eg. extracts `region` from `inn`) and applies error filters to remove 
some rows and make `<year>.csv`.

## Variables

The Rosstat dataset contains balance sheet, profit and loss ('P&L') and cash flow ('CF') statement variables. Each variable is a column in dataframe. 


```
print({c:boo.whatis(c) for c in df.columns if "_lag" no in c})
```

TODO:
- make a generator for variable list table

## Data sources

## Hints

#### User

- CSV files are quite big, start with year 2012 to experiment.
- Use link above for Google Colab to run package remotely.
- Use `read_dataframe(year)` to read canonic CSV file. 

#### Developper

- `boo.path.default_data_folder` shows where the CSV files are on a computer.
- `boo.columns` controls CSV column selection and naming.
- `boo.dataframe.canonic` makes canonic CSV. By coincidence the outputhas same number of columns as `<year>.csv`, but the columns are slightly different as some columns are added and some removed.
- `boo.year.TIMESTAMPS` help to find proper URLs, which change along with Rosstat website updates. 
- New annual dataset released around September-October.

## Script

Rosstat publishes CSV files without column headers. 
When preparing a readable CSV file we assign a name to columns
with variables of interest and cut away the rest of the columns. 

This way we get a much smaller file (~50% of the size). We can read 
and manipulate data from this this file using pandas or R. 

For illustration, batch script below creates `2012.csv` file with column names.

```bat
set url=http://www.gks.ru/opendata/storage/7708234640-bdboo2012/data-20190329t000000-structure-20121231t000000.csv
set index=1,2,3,4,5,6,7,8,17,18,27,28,37,38,41,42,43,44,57,58,59,60,67,68,69,70,79,80,81,82,83,84,93,94,99,100,105,106,117,118,204,205,209,210,211,212,213,214,215,216,222,223,228,229,235,240,241,266 
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
build(2012)
```

## Limitations

- No timeseries: we can access cross-section of all data by year, but not several years of data by each firm. 
- No database: we store files as plain CSV, not in a database.

## Contributors

The package is maintained by [Evgeniy Pogrebnyak](https://github.com/epogrebnyak).

Special thanks to [Daniil Chizhevskij](https://daniilchizhevskij.ml/) for PyPI collaboration. Without his support `pip install boo` would not be possible.
