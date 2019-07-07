# TODO: pip install boo

import pandas as pd
from columns import CONVERTER_FUNC as shorten, SHORT_COLUMNS
from file import curl, yield_rows, save_rows
from path import raw, processed, canonical
from year import make_url

def preclean(path, force: bool):
    """Delete an exisiting file if *force* flag is set to True"""
    if force is True and path.exists():
       path.unlink()

def download(year: int, force=False):
    """Download file from Rosstat."""
    path, url = raw(year), make_url(year), 
    preclean(path, force)
    print("Downloading", url)
    curl(path, url)
    print("Saved as", path)
    # MAYBE: show line count  

     
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


def dataframe(path, dtypes):
    with open(path, 'r', encoding='utf-8') as f:
        return pd.read_csv(f, dtype=dtypes)  
    
    
def read_intermediate_df(year: int):
    src = processed(year)    
    return dataframe(src, SHORT_COLUMNS.dtypes)


def make_canonical_df(year: int, worker, column_names, force=False):
    df = read_intermediate_df(year)    
    # TODO: add parsing logic here from row.py
    # MAYBE: save dtypes as json, use them if available to speed up df import  
    dst = canonical(year)
    pass   


def read_df(year):
    src = canonical(year)
    # TODO: use types list
    return dataframe(src)


# Shorthand functions
    
def cut(year: int, force=False):
    cut_columns(year, force=force)


def put(year: int, force=False):
    pass
    # make_canonical_df(year, force)


def acquire(year: int, force=False):
    download(year)
    cut(year)
    put(year)    
    
if __main__ == "__name__":
    from year import YEARS
    for year in YEARS:
        acquire(year, True)    