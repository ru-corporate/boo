[![PyPI](https://img.shields.io/pypi/v/boo.svg)](https://pypi.python.org/pypi/boo/#history)
[![Python package](https://github.com/ru-corporate/boo/actions/workflows/.action.yml/badge.svg)](https://github.com/ru-corporate/boo/actions/workflows/.action.yml)
[![Coverage Status](https://coveralls.io/repos/github/ru-corporate/boo/badge.svg?branch=master&service=github)](https://coveralls.io/github/ru-corporate/boo?branch=master)
[![Downloads](https://pepy.tech/badge/boo)](https://pepy.tech/project/boo)
[![на русском](https://img.shields.io/badge/README-%D1%80%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9-blue)](README.ru.md)

# boo

`boo` is a Python client to download and transform annual corporate reports of 2.5 million Russian firms.

`boo` is an acronym for _'accounting reports of organisations'_ (in Russian 'бухгалтерская отчетность организаций'),
a term Rosstat uses for original datasets.

The dataset is limited to 2012-2018, as later years now require paid subscription.

## Install

```
pip install boo
```

For development version:

```
pip install git+https://github.com/ru-corporate/boo.git@master
```

## Usage

### Download and read dataframe

```python
from boo import download, unpack, read_dataframe

download(2012)
unpack(2012)
df = read_dataframe(2012, nrows=100)
print(df.head())
```

### Colab example 

 [The following ![colab](https://img.shields.io/badge/colab-launch-blue.svg) notebook][nes2020]
 was used in NES corporate banking course in spring 2020, it demonstartes some possibilites of the dataset.

[nes2020]: https://colab.research.google.com/drive/1ndEekNo9V2rjNuLWdeWfT9b4pdJqjlWk#scrollTo=UsdxxSKTP7Io

## Files

CSV files are located at `~/.boo` folder. 

`df = read_dataframe(year)` returns a reference ("canonic") dataset, that is suggested as a starting point for analysis. `read_dataframe(year)` reads `<year>.csv`, transforms some columns (for example, extracts `region` from `inn`) and applies filters to remove erroneous rows. Tax identificator (`inn`) used as an index.

If you want to see `<year>.csv` raw content without transformation or corrections, use `read_intermediate_df(year)`. 

### Years and file size

Suported years and file sizes are listed below. 


|   Year |   ZIP (Mb) |   CSV (Mb) |
|-------:|-----------:|-----------:|
|   2012 |         84 |        513 |
|   2013 |        187 |       1162 |
|   2014 |        215 |       1318 |
|   2015 |        250 |       1565 |
|   2016 |        256 |       1588 |
|   2017 |        261 |       1595 |
|   2018 |        257 |       1550 |


You can use `boo.file_length(year)` to check raw file sizes from Rosstat website. 

```python
>> from boo import file_length
>> file_length(2017) # size in bytes
1671752977
```

## Variables

The Rosstat dataset contains balance sheet, profit and loss and cash flow statement variables. Each variable is a column in dataframe. 

```python
>>> {c:boo.whatis(c) for c in df.columns if "_lag" not in c}

{'title': 'Короткое название организации',
 'org': 'Тип юридического лица (часть наименования организации)',
 'okpo': 'Общероссийский классификатор предприятий и организаций (ОКПО)',
 'okopf': 'Общероссийский классификатор организационно-правовых форм (ОКОПФ)',
 'okfs': 'Общероссийский классификатор форм собственности (ОКФС)',
 'okved': 'Общероссийский классификатор видов экономической деятельности (ОКВЭД)',
 'unit': 'Код единицы измерения (384 - тыс. руб.)',
 'ok1': 'Код ОКВЭД первого уровня',
 'ok2': 'Код ОКВЭД второго уровня',
 'ok3': 'Код ОКВЭД третьего уровня',
 'region': 'Код региона по ИНН',
 'of': 'Основные средства',
 'ta_fix_fin': 'Финансовые вложения',
 'ta_fix': 'Итого внеоборотных активов',
 'inventory': 'Запасы',
 'receivables': 'Дебиторская задолженность',
 'ta_nonfix_fin': 'Финансовые вложения (за исключением денежных эквивалентов)',
 'cash': 'Денежные средства и денежные эквиваленты',
 'ta_nonfix': 'Итого оборотных активов',
 'ta': 'БАЛАНС (актив)',
 'retained_earnings': 'Резервный капитал',
 'tp_capital': 'Итого капитал',
 'debt_long': 'Долгосрочные заемные средства',
 'tp_long': 'Итого долгосрочных обязательств',
 'debt_short': 'Краткосрочные заемные обязательства',
 'payables': 'Краткосрочная кредиторская задолженность',
 'tp_short': 'Итого краткосрочных обязательств',
 'tp': 'БАЛАНС (пассив)',
 'sales': 'Выручка',
 'costs': 'Себестоимость продаж',
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
 'cf_oper': 'Сальдо денежных потоков от текущих операций',
 'cf_inv_in': 'Поступления - всего',
 'cf_inv_out': 'Платежи - всего',
 'paid_fa_investment': 'В связи с приобретением, созданием, модернизацией, реконструкцией и подготовкой к использованию внеоборотны активов',
 'cf_inv': 'Сальдо денежных потоков от инвестиционных операций',
 'cf_fin_in': 'Поступления - всего',
 'cf_loan_in': 'Получение кредитов и займов',
 'cf_eq_in_1': 'Денежных вкладов собственников (участников)',
 'cf_eq_in_2': 'От выпуска акций, увеличения долей участия',
 'cf_bond_in': 'От выпуска облигаций, векселей и других долговых ценных бумаг и др.',
 'cf_fin_out': 'Платежи - всего',
 'cf_eq_out': 'Собственникам (участникам) в связи с выкупом у них акций (долей участия) организации или их выходом из состава участников',
 'cf_div_out': 'На уплату дивидендов и иных платежей по распределению прибыли в пользу собственников (участников)',
 'cf_debt_out': 'В связи с погашением (выкупом) векселей и других долговы ценных бумаг, возврат кредитов и займов',
 'cf_fin': 'Сальдо денежных потоков от финансовых операций',
 'cf': 'Сальдо денежных потоков за отчетный период'}```

## Hints

#### User

- CSV files are quite big, start with year 2012 to experiment.
- Use link above for Google Colab to run package remotely. It runs fairly quickly.
- Use `read_dataframe(year)` to read canonic CSV file. 
- Several filters and utility functions are avilable from `boo.dataframe.filter` and `boo.dataframe.util`.

#### Developper

- `boo.default_data_folder()` shows where the ZIP and CSV files are on a computer.
- `boo.columns` controls CSV column selection and naming.
- `boo.dataframe.canonic` makes canonic CSV. By coincidence the output has same number of columns as `<year>.csv`, but the columns are indeed different as some columns are added and some removed.

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

The package was created by [Evgeniy Pogrebnyak](https://github.com/epogrebnyak).

Special thanks to [Daniil Chizhevskij](https://daniilchizhevskij.ml/) for PyPI collaboration. Without his support `pip install boo` would not be possible.
