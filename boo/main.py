# TODO:
# - [ ] variable descriptions boo.whatis
# - [ ] tests, existing and new
# - [ ] subsets
# - [ ] visuals

# MAYBE:
# - [ ] larger dummy example to load, 50 + 50 + 1000 example
# - [ ] download() can show line count
# - [ ] download() must fail on small fail on small file or HTML file
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
# - [ ] pip install boo
# - [x] autopep8
# - [x] okved


import pandas as pd

from boo.year import YEARS, make_url
from boo.file import curl, yield_rows, save_rows
from boo.path import raw, processed, canonic
from boo.columns import CONVERTER_FUNC as shorten, SHORT_COLUMNS
from boo.dataframe import canonic_df, canonic_dtypes


def preclean(path, force: bool):
    """Delete an exisiting file if *force* flag is set to True"""
    if force is True and path.exists():
        path.unlink()


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


def write_df(df, path):
    df.to_csv(
        path,
        index=False,
        header=True,
        chunksize=100_000,
        encoding='utf-8')


def read_intermediate_df(year: int):
    src = processed(year)
    return read_df(src, SHORT_COLUMNS.dtypes)


def make_canonic_df(year: int, force=False):
    dst = canonic(year)
    preclean(dst, force)
    print(f"Reading intermediate dataframe for {year}...")
    df = canonic_df(read_intermediate_df(year))
    print(f"Created final dataframe for {year}")
    print(f"Saving to {dst}...")
    write_df(df, dst)
    print("Done")
    return dst


def read_canonic_df(year):
    src = canonic(year)
    return read_df(src, dtypes=canonic_dtypes())


# Shorthand functions


def cut(year: int):
    return cut_columns(year, force=False)


def cutf(year: int):
    return cut_columns(year, force=True)


def put(year: int):
    return make_canonic_df(year, force=False)


def putf(year: int):
    return make_canonic_df(year, force=True)


def read_dataframe(year):
    return read_canonic_df(year)


def frame(year: int):
    return read_canonic_df(year)


def prepare(year: int):
    if not raw(year).exists():
        download(year)
    if not processed(year).exists():
        cut(year)
    if not canonic(year).exists():
        put(year)


def quiet_delete(file):
    if file.exists():
        file.unlink()


def wipe(year):
    quiet_delete(raw(year))
    quiet_delete(processed(year))


def wipe_all(year):
    wipe(year)
    quiet_delete(canonic(year))


def prepare_all():
    for year in YEARS:
        prepare(year)
