"""
Basic use:
    prepare(year)
    read_dataframe(year)
    
Helpers:
    whatis(column_name)
    location(year)        

Notes: 
- prepare() is an alias to run two functions download(year) and  build(year)
"""
import pandas as pd
from pathlib import Path

from boo.year import make_url
from boo.path import raw, processed
from boo.file import curl, yield_rows, save_rows
from boo.columns import CONVERTER_FUNC, SHORT_COLUMNS
from boo.dataframe.canonic import canonic_df
from boo.messages import help_download_force, help_build_force

def preclean(path, force: bool):
    """Delete an exisiting file if *force* flag is set to True"""
    if force is True and path.exists():
        path.unlink()


def download(year: int, force=False):
    """Download file from Rosstat."""
    path, url = raw(year), make_url(year),
    preclean(path, force)
    print(f"Downloading source file for {year} from ", url)
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

def prepare(year: int):
    r = raw(year)
    if not r.exists():
        download(year)
    else:    
        print("Already downloaded:", r)
        print (help_download_force(year))
    p = processed(year)
    if not p.exists():
        build(year)
    else: 
        print("Already built:", p)
        print (help_build_force(year))
        
        
def wipe(path_str):
    file = Path(path_str)
    if file.exists():
        file.unlink()
        

def locate_raw(year):
    return str(raw(year))

    
def locate_processed(year):
    return str(processed(year))  