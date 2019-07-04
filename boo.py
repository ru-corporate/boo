import pandas as pd
from columns import shorten, COLUMNS_SHORT, DTYPES_SHORT
from file import curl, yield_rows, save_rows
from paths import raw, processed
from year import make_url

# FIXME: must fail of downloading an HTML

def download(year, force=False):
    """Download file from Rosstat."""
    path, url = raw(year), make_url(year), 
    if force:
       path.unlink()
    print("Downloading", url)
    curl(path, url)
    print("Saved as", path)
    return path       
       

def cut(year, worker=shorten, column_names=COLUMNS_SHORT, force=False):
    """Create local file with fewer columns. 
       Columns in new file will be named according to *COLUMNS_SHORT*.
       Rows will be modified with *worker* function.
    """    
    src, dst = raw(year), processed(year)
    if force:
       dst.unlink()
    print("Reading from", dst)    
    print("Saving to", dst)    
    save_rows(path=dst, 
              stream=map(worker, yield_rows(src)), 
              column_names=column_names)
    print("Done")  


def dataframe(path, dtypes):
    with open(path, 'r', encoding='utf-8') as f:
        return pd.read_csv(f, dtype=dtypes)  

    
def read_processed_df(year):
    src = processed(year)    
    return dataframe(src, DTYPES_SHORT)

# FIXME: move parsing logic here

def read_canonical_df(year):
    pass