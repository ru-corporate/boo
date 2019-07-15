# TODO:
# - [ ] variable descriptions boo.whatis
# - [ ] port existing tests
# - [ ] subsets
# - [ ] visuals

# MAYBE:
# - [ ] larger dummy example to load, 50 + 50 + 1000 example
# - [ ] download() must fail on small fail on small file or HTML file

# NO:
# - [ ] download() can show line count
# - [ ] save dtypes as json, use them if available to speed up df import


# MAYBE: add descriptions
# def new_text_field_name(varname: str):
#    okv = lambda text: f"Код ОКВЭД {text} уровня"
#    return {'ok1': okv("первого"),
#            'ok2': okv("второго"),
#            'ok3': okv("третьего"),
#            'org': "Тип юридического лица (часть наименования организации)",
#            'title': "Короткое название организации",
#            'region': "Код региона по ИНН"}.get(varname)

# DONE:
# - [x] boo vs . in backage
# - [x] pip install boo
# - [x] autopep8
# - [x] okved v2


import pandas as pd

from boo.year import make_url
from boo.path import raw, processed
from boo.file import curl, yield_rows, save_rows
from boo.columns import CONVERTER_FUNC as shorten, SHORT_COLUMNS
from boo.dataframe import canonic_df

def preclean(path, force: bool):
    """Delete an exisiting file if *force* flag is set to True"""
    if force is True and path.exists():
        path.unlink()


def quiet_delete(file):
    if file.exists():
        file.unlink()


def wipe_raw(year):
    quiet_delete(raw(year))

    
def wipe_processed(year):
    quiet_delete(processed(year))


def download(year: int, force=False):
    """Download file from Rosstat."""
    path, url = raw(year), make_url(year),
    preclean(path, force)
    print("Downloading", url, f"for {year}")
    curl(path, url)
    print("Saved as", path)
    return path


def cut_columns(year, worker=shorten, column_names=SHORT_COLUMNS.all,
                force=False):
    """Create smaller local file with fewer columns.
       Columns will be named with *COLUMNS_SHORT*.
       Rows will be modified by *worker* function.
    """
    src, dst = raw(year), processed(year)
    preclean(dst, force)
    print("Reading from", src)
    print("Saving to", dst)
    save_rows(path=dst,
              stream=map(worker, yield_rows(src)),
              column_names=column_names)
    print("Done")
    return dst


def read_df(path, dtypes):
    with open(path, 'r', encoding='utf-8') as f:
        return pd.read_csv(f, dtype=dtypes)


def read_intermediate_df(year: int):
    src = processed(year)
    return read_df(src, SHORT_COLUMNS.dtypes)


def read_dataframe(year):
    return canonic_df(read_intermediate_df(year))

# Shorthand functions

def cut(year: int):
    return cut_columns(year, force=False)


def cutf(year: int):
    return cut_columns(year, force=True)


def prepare(year: int):
    if not raw(year).exists():
        download(year)
    if not processed(year).exists():
        cut(year)