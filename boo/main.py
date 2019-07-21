"""
Basic use:
    prepare(year)
    read_dataframe(year)

Helpers:
    whatis(column_name)
    locate(year)
    inspect(year)

Notes:
- prepare() is an alias to run both download(year) and build(year)
"""

from boo.year import make_url
from boo.path import locate
from boo.file import curl, yield_rows, save_rows, read_df
from boo.columns import CONVERTER_FUNC, SHORT_COLUMNS
from boo.dataframe.canonic import canonic_df
from boo.messages import help_force


def preclean(path, force: bool):
    """Delete an exisiting file if *force* flag is set to True"""
    if force is True and path.exists():
        path.unlink()


def download(year: int, force=False):
    """Download file from Rosstat."""
    path, url = locate(year).raw, make_url(year),
    preclean(path, force)
    print(f"Downloading source file for {year} from", url)
    curl(path, url)
    print("Saved as", path)
    return path


def build(year, force=False,
          worker=CONVERTER_FUNC,
          column_names=SHORT_COLUMNS.all):
    """Create smaller CSV file with fewer columns.
       Columns have names *COLUMNS_SHORT*.
       Rows will be modified by *worker* function.
    """
    src, dst = locate(year).raw, locate(year).processed
    preclean(dst, force)
    print("Reading from", src)
    print("Saving to", dst)
    save_rows(path=dst,
              stream=map(worker, yield_rows(src)),
              column_names=column_names)
    print("Done")
    return dst


def read_intermediate_df(year: int):
    src = locate(year).processed
    return read_df(src, SHORT_COLUMNS.dtypes)


def read_dataframe(year):
    return canonic_df(read_intermediate_df(year))


def prepare(year: int):
    r = locate(year).raw
    if not r.exists():
        download(year)
    else:
        print("Already downloaded:", r)
        print(help_force(year, "download"))
    p = locate(year).processed
    if not p.exists():
        build(year)
    else:
        print("Already built:", p)
        print(help_force(year, "build"))