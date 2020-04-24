"""
Basic use:
    download(year)
    build(year)
    read_dataframe(year)

Helper:
    inspect(year)
"""

import numpy as np
import pandas as pd

from boo.year import make_url
from boo.path import RawFile
from boo.curl import curl
from boo.columns import INDEX, NAMES
from boo.dataframe.canonic import canonic_df


def conditional_delete(path, force: bool):
    """Delete an exisiting file at *path* if *force* flag is set to True"""
    if force is True and path.exists():
        path.unlink()
        print("Deleted", path)


def force_message(year, verb):
    return f"Use {verb}({year}, force=True) to overwrite existing file."


def download(year: int, force=False, directory=None):
    """Download file from Rosstat web site."""
    raw_file = RawFile(year, directory)
    path = raw_file.path
    url = make_url(year)
    conditional_delete(path, force)
    if not path.exists():
        print(f"Downloading source file for {year} from", url)
        curl(path, url)
        print("Saved as", raw_file)
    else:
        print("Already downloaded:", raw_file)
        print(force_message(year, "download"))
    return path


def download_direct(url: str, year: int, force=False, directory=None):
    raw_file = RawFile(year, directory)
    path = raw_file.path
    conditional_delete(path, force)
    if not path.exists():
        print(f"Downloading source file for {year} from {url}")
        curl(path, url)
        print("Saved as", raw_file)
    else:
        print("Already downloaded:", raw_file)
        print(force_message(year, "download"))
    return path


def read_intermediate_df(year: int, directory=None, **kwargs):
    src = RawFile(year, directory).path
    print(f"Reading dataframe from {src}")
    return pd.read_csv(
        src,
        encoding="windows-1251",
        sep=";",
        header=None,
        usecols=INDEX,  # read only a subset of columns
        names=[x for x in NAMES.keys()],  # give new names to these columns
        # ERROR:
        # Shutting down dtypes temporarliy due to https://github.com/ru-corporate/boo/issues/18
        #dtype=NAMES,  # enforce string or int types
        **kwargs,
    )


def read_dataframe(year: int, directory=None, **kwargs):
    """Read canonic data for *year* as dataframe.

    Returns:
        pandas.DataFrame
    """
    return canonic_df(read_intermediate_df(year, directory, **kwargs))


def inspect(year: int, directory=None):
    """Diagnose local data file for *year*."""
    raw = RawFile(year, directory)
    if raw.exists():
        print(f"      Raw CSV file: {raw}")
        if raw.mb() < 1:
            print(
                "WARNING: file size too small. "
                "Usually file size is larger than 500Mb."
            )
    else:
        raw.print_error()
    return str(raw.path)
