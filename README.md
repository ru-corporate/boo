[![PyPI](https://img.shields.io/pypi/v/boo.svg)](https://pypi.python.org/pypi/boo/#history)
[![Build Status](https://travis-ci.com/ru-corporate/boo.svg?branch=master)](https://travis-ci.com/ru-corporate/boo)
[![Coverage Status](https://coveralls.io/repos/github/ru-corporate/boo/badge.svg?branch=master&service=github)](https://coveralls.io/github/ru-corporate/boo?branch=master)
[![на русском](https://img.shields.io/badge/README-%D1%80%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9-blue)](README.ru.md)

# boo

`boo` is a Python client to download and transform annual corporate reports of 2.5 million Russian firms.

`boo` is an acronym for _'accounting reports of organisations'_ (in Russian 'бухгалтерская отчетность организаций'),
a term Rosstat uses for original datasets.


## Install

```
pip install boo
```

For development version:

```
pip install git+https://github.com/ru-corporate/boo.git@master
```

## Usage

### Download and read full dataframe

```python
from boo import download, read_dataframe

download(2012)
df = read_dataframe(2012)
print(df.head())
```

### Colab example 

 [The following ![colab](https://img.shields.io/badge/colab-launch-blue.svg) notebook][nes2020]
 was used in NES corporate banking course in spring 2020.

[nes2020]: https://colab.research.google.com/drive/1ndEekNo9V2rjNuLWdeWfT9b4pdJqjlWk#scrollTo=UsdxxSKTP7Io


### Documentation

<https://ru-corporate.github.io/boo/>


## Files

CSV files are located at `~/.boo` folder. Function `boo.locate(year)` will show exactly where they are.


File name     | Description  | Column count |  Created by 
--------------|--------------|:------------:|:------------:
`raw<year>.csv` | Original CSV file from Rosstat website. No header row.    | 266 | `download(year)`
`<year>.csv` | CSV file with column names in header row.  | 58 | `build(year)`

`boo.build()` takes `raw<year>.csv` and creates a local CSV file `<year>.csv` with column names.  `<year>.csv` is importable as pandas dataframe. 

`df = read_dataframe(year)` returns a reference ("canonic") dataset, that is suggested as a starting point for analysis. 
`read_dataframe(year)` reads `<year>.csv`, transforms some columns (for example, extracts `region` from `inn`) and applies filters to remove erroneous rows. Tax identificator (`inn`) used as an index.

If you want to see `<year>.csv` raw content without transformation or corrections, use `read_intermediate_df(year)`. 

### Years and file size

Suported years are listed below. Raw file sizes are from 500Mb to 1.6Gb. 

|   Year |   Size (Mb) |
|--------|-------------|
|   2012 |         513 |
|   2013 |        1162 |
|   2014 |        1318 |
|   2015 |        1565 |
|   2016 |        1588 |
|   2017 |        1594 |
|   2018 |        1549 |

You can use `boo.file_length(year)` and `boo.file_length_mb(year)` to retrieve raw file sizes from Rosstat website. 

```python
>> from boo import file_length, file_length_mb
>> file_length(2017) # size in bytes
1671752977

>> file_length_mb(2017) # size in Mb
1594
```

## Variables

The Rosstat dataset contains balance sheet, profit and loss and cash flow statement variables. Each variable is a column in dataframe. 

```python
>>> {c:boo.whatis(c) for c in df.columns if "_lag" not in c}

{'title': 'Короткое название организации',
 'org': 'Тип юридического лица (часть наименования организации)',
 'okpo': None,
 'okopf': None,
 'okfs': None,
 'okved': None,
 'unit': None,
 'ok1': 'Код ОКВЭД первого уровня',
 'ok2': 'Код ОКВЭД второго уровня',
 'ok3': 'Код ОКВЭД третьего уровня',
 'region': 'Код региона по ИНН',
 'of': 'Основные средства',
 'ta_fix': 'Итого внеоборотных активов',
 'cash': 'Денежные средства и денежные эквиваленты',
 'ta_nonfix': 'Итого оборотных активов',
 'ta': 'БАЛАНС (актив)',
 'tp_capital': 'Итого капитал',
 'debt_long': 'Долгосрочные заемные средства',
 'tp_long': 'Итого долгосрочных обязательств',
 'debt_short': 'Краткосрочные заемные обязательства',
 'tp_short': 'Итого краткосрочных обязательств',
 'tp': 'БАЛАНС (пассив)',
 'sales': 'Выручка',
 'profit_oper': 'Прибыль (убыток) от продаж',
 'exp_interest': 'Проценты к уплате',
 'profit_before_tax': 'Прибыль (убыток) до налогообложения',
 'profit_after_tax': 'Чистая прибыль (убыток)',
 'cf_oper_in': 'Поступления - всего',
 'cf_oper_in_sales': 'От продажи продукции, товаров, работ и услуг',
 'cf_oper_out': 'Платежи - всего',
 'paid_to_supplier': 'Поставщикам (подрядчикам) за сырье, материалы, работы, услуги',
 'paid_to_worker': 'В связи с оплатой труда работников',
 'paid_interest': 'Проценты по долговым обязательствам',
 'paid_profit_tax': 'Налога на прибыль организаций',
 'paid_other_costs': 'Прочие платежи',
 'cf_oper': 'Сальдо денежных потоков от текущих операций',
 'cf_inv_in': 'Поступления - всего',
 'cf_inv_out': 'Платежи - всего',
 'paid_fa_investment': 'В связи с приобретением, созданием, модернизацией, реконструкцией и подготовкой к использованию внеоборотны активов',
 'cf_inv': 'Сальдо денежных потоков от инвестиционных операций',
 'cf_fin_in': 'Поступления - всего',
 'cf_fin_out': 'Платежи - всего',
 'cf_fin': 'Сальдо денежных потоков от финансовых операций',
 'cf': 'Сальдо денежных потоков за отчетный период'}
```

## Hints

#### User

- CSV files are quite big, start with year 2012 to experiment.
- Use link above for Google Colab to run package remotely. It runs fairly quickly.
- Use `read_dataframe(year)` to read canonic CSV file. 
- Several filters and utility functions are avilable from `boo.dataframe.filter` and `boo.dataframe.util`.

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


### Slightly advanced use: data filters for smaller subsets

```python
from boo.dataframe.filter import (large_companies, 
                                  minimal_columns, 
                                  shorthand)
df2 = shorthand(minimal_columns(large_companies(df)))
print(df2.head())
```

## Contributors

The package is maintained by [Evgeniy Pogrebnyak](https://github.com/epogrebnyak).

Special thanks to [Daniil Chizhevskij](https://daniilchizhevskij.ml/) for PyPI collaboration. Without his support `pip install boo` would not be possible.
