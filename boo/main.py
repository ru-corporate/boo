"""
Basic use:
    download(year)
    build(year)
    read_dataframe(year)

Helpers:
    whatis(column_name)
    locate(year)
    inspect(year)
"""

from boo.year import make_url
from boo.path import locate
from boo.curl import curl
from boo.file import yield_rows, save_rows, read_df
from boo.columns import CONVERTER_FUNC, SHORT_COLUMNS
from boo.dataframe.canonic import canonic_df


def preclean(path, force: bool):
    """Delete an exisiting file if *force* flag is set to True"""
    if force is True and path.exists():
        path.unlink()


def help_force(year, verb):
    return f"Use {verb}({year}, force=True) to overwrite existing file."


class FileNotDownloadedError(FileNotFoundError):
    pass


def check_downloaded(path):
    if not path.exists():
        raise FileNotDownloadedError(path)


def download(year: int, force=False, directory=None):
    """Download file from Rosstat web site."""
    raw_file = locate(year, directory).raw
    path = raw_file.path
    url = make_url(year)
    preclean(path, force)
    if not path.exists():
        print(f"Downloading source file for {year} from", url)
        curl(path, url)
        print("Saved as", raw_file)
    else:
        print("Already downloaded:", raw_file)
        print(help_force(year, "download"))
    return path


def build(year, force=False, directory=None,
          worker=CONVERTER_FUNC,
          column_names=SHORT_COLUMNS.all):
    """Create smaller CSV file with fewer columns.
       Columns have names as in *COLUMNS_SHORT*.
       Rows will be modified by *worker* function.
    """
    loc = locate(year, directory)
    src, dst = loc.raw, loc.processed
    check_downloaded(src)
    preclean(dst.path, force)
    if not dst.exists():
        print("Reading from", src)
        print("Saving to", dst)
        save_rows(path=dst.path,
                  stream=map(worker, yield_rows(src.path)),
                  column_names=column_names)
        print("Saved", dst)
    else:
        print("Already built:", dst)
        print(help_force(year, "build"))


def read_intermediate_df(year: int, directory=None):
    src = locate(year, directory).processed
    return read_df(src.path, SHORT_COLUMNS.dtypes)


def read_dataframe(year: int, directory=None):
    """Read canonic data for *year* as dataframe.

    Returns:
        pandas.DataFrame
    """
    return canonic_df(read_intermediate_df(year, directory))


def inspect(year: int, directory=None):
    print("URL:", make_url(year))
    loc = locate(year, directory)
    for x in [loc.raw, loc.processed]:
        for msg in x.state():
            print(msg)
