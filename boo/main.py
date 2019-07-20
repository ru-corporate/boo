"""
Minimum use:
    prepare(year)
    read_dataframe(year)
    
Helpers:
    whatis(column_name)
    location(year)        

Prepare is an alias to run two functions:
    download(year)
    build(year)
"""
# TODO:
# - [ ] variable descriptions boo.whatis
# - [ ] 
# - [ ] port existing tests
# - [ ] subsets
# - [ ] visuals
# - [ ] analysis quality criteria

# MAYBE:
# - [ ] larger dummy example to load, 50 + 50 + 1000 example
# - [ ] download() must fail on small fail on small file or HTML file

# NO:
# - [ ] download() can show line count
# - [ ] save dtypes as json, use them if available to speed up df import

# - [ ] save of canonic non-empty files

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
from pathlib import Path

from boo.year import make_url
from boo.path import raw, processed
from boo.file import curl, yield_rows, save_rows
from boo.columns import CONVERTER_FUNC, SHORT_COLUMNS
from boo.dataframe.canonic import canonic_df

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

# message system

def filesize(path):
    return round(path.stat().st_size / (1024 * 1024.0), 1)

    
def help_download_force(year):
    return f"Use download({year}, force=True) to overwrite existing file."


def help_build_force(year):
    return "Use build({year}, force=True) to overwrite existing file."


def help_download(year):
    return f"Use download({year}) to download raw CSV file."


def help_build(year):
    return f"Use build({year}) to create readable file."

def help_df(year):
    return f"Use df = read_dataframe({year}) to read it as pandas dataframe."


      
class Dataset:    
    def __init__(self, year):
        self.year = year
        self.url = make_url(year)
        self.raw = raw(year)
        self.processed = processed(year)
        
    def is_downloaded(self):
        return self.raw.exists()
    
    def is_built(self):
        return self.processed.exists() 
    
    def raw_state(self):
        if self.is_downloaded():            
            size = filesize(self.raw)
            yield f"Raw file downloaded as {self.raw} ({size}M)"
            if size < 1:
                yield "WARNING: file size too small. " + help_download_force(self.year)
        else:
            yield "Raw file not downloaded. " + help_download(self.year)                
                
    def processed_state(self):
        if self.is_built():
            size = filesize(self.processed)
            yield f"Processed CSV file is saved as {self.processed} ({size}M)"
            yield help_df(self.year)
        else:
            yield "Final file not built. " + help_build(self.year)
            

def inspect(year: int):
    d = Dataset(year)
    print ("Year:", year)
    print ("Raw file URL:", d.url)
    print()
    for msg in d.raw_state():
        print (msg)
    print()
    for msg in d.processed_state():
        print (msg)  
                        