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


class NoRawFileError(FileNotFoundError):
    def __init__(self, year):
        super().__init__(
            f"Raw CSV file not downloaded for {year}. "
            f"Try `boo.download({year})`.")


class NoProcessedFileError(FileNotFoundError):
    def __init__(self, year):
        super().__init__(
            f"Final CSV file not built for {year}. "
            f"Try `boo.build({year})`."
        )


def check_is_downloaded(year, directory=None):
    if not locate(year, directory).raw.exists():
        raise NoRawFileError(year)


def check_is_built(year, directory=None):
    if not locate(year, directory).processed.exists():
        raise NoProcessedFileError(year)


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
    if dst.exists() and not force:
        print("Already built:", dst)
        print(help_force(year, "build"))
        return
    preclean(dst.path, force)
    check_is_downloaded(year, directory)
    if not dst.exists():
        print("Reading from", src)
        print("Saving to", dst)
        save_rows(path=dst.path,
                  stream=map(worker, yield_rows(src.path)),
                  column_names=column_names)
        print("Saved", dst)


def read_intermediate_df(year: int, directory=None):
    check_is_built(year, directory)
    src = locate(year, directory).processed
    return read_df(src.path, SHORT_COLUMNS.dtypes)


def read_dataframe(year: int, directory=None):
    """Read canonic data for *year* as dataframe.

    Returns:
        pandas.DataFrame
    """
    return canonic_df(read_intermediate_df(year, directory))


def inspect(year: int, directory=None):
    is_downloaded, is_processed = False, False
    print("URL:", make_url(year))
    loc = locate(year, directory)
    if loc.raw.exists():
        is_downloaded = True
        print(f"Raw CSV file: {loc.raw}")
        if loc.raw.mb() < 1:
            print("WARNING: file size too small. "
                  "Usual size is larger than 500Mb.")
    try:
        check_is_downloaded(year, directory)
    except NoRawFileError as e:
        print(e)
    if loc.processed.exists():
        is_processed = True
        print(f"Processed CSV file: {loc.processed}")
        print(f"Use `df=boo.read_dataframe({year})` next.")
    try:
        check_is_built(year, directory)
    except NoProcessedFileError as e:
        print(e)
    return is_downloaded, is_processed
