"""Availabale years and URLs for them."""

import requests
from tqdm import tqdm
from typing import List
from urllib.request import urlopen
from pathlib import Path
import pandas as pd
from dataclasses import dataclass
#from boo.columns import INDEX, NAMES
from zipfile import ZipFile
from typing import Optional


# Note: must manually hardcode new timestamps when new version of data arrives.


def timestamps(year):
    return {
        2012: ("7708234640-", "20200331"),  # different
        2013: ("7708234640-", "20200331"),  # different
        2014: ("7708234640-", "20200327"),
        2015: ("7708234640-", "20200327"),
        2016: ("7708234640-", "20200327"),
        2017: ("7708234640-", "20200327"),
        2018: ("7708234640-7708234640", "20200327"),  # different
    }[year]

def required_file_size(year):
    return {
        2012: 88_169_551,
        2013: 195_986_142,
        2014: 225_816_835,
        2015: 262_173_543,
        2016: 268_515_446,
        2017: 273_328_344,
        2018: 269_452_075  
    }[year]

def filename(year):
    _, timestamp = timestamps(year)
    return f"data-{timestamp}-structure-{year}1231"


def csv_filename(year):
    return filename(year) + ".csv"


assert csv_filename(2012) == "data-20200331-structure-20121231.csv"


def mk_url(year):
    if year == 0:
        return "" # for testing
    if year == 1:
        return "" # for testing
    mid, timestamp = timestamps(year)
    return (
        "https://rosstat.gov.ru/opendata/"
        f"{mid}bdboo{year}/"
        f"data-{timestamp}-structure-{year}1231.zip"
    )

assert mk_url(2018)=="https://rosstat.gov.ru/opendata/7708234640-7708234640bdboo2018/data-20200327-structure-20181231.zip"

def available_years() -> List[int]:
    """List available years with datasets."""
    return list(range(2012, 2018 + 1))


def curl(path: str, url: str, n_chunks=None):
    r = requests.get(url, stream=True)
    iterable = tqdm(r.iter_content(chunk_size=1024), unit=" k")
    with open(path, "wb") as f:
        i = 0
        for chunk in iterable:
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
            i += 1
            if n_chunks and i >= n_chunks:
                break


def url_content_length(url: str) -> int:
    with urlopen(url) as f:
        return int(f.info()["Content-Length"])


def file_length(year: int):
    return url_content_length(url=mk_url(year))


def unzip(path):
    with ZipFile(path) as zf:
        zf.extractall(default_data_folder())
        return zf.namelist()


def default_data_folder() -> Path:
    home = Path.home() / ".boo"
    home.mkdir(exist_ok=True)
    return home


def path_zip(year: int, folder: Path):
    return folder / f"{year}.zip"


def path_csv(year: int, folder: Path):
    return folder / csv_filename(year)


def download_zip(year):
    curl(path_zip(year), mk_url(year))


def read_intermediate_df(year, **kwargs):
    # can use read_intermediate_df(year, nrows=100) for small example
    path = path_csv(year)
    return pd.read_csv(
        path,
        encoding="windows-1251",
        sep=";",
        header=None,
        usecols=INDEX,  # read only a subset of columns
        names=[x for x in NAMES.keys()],  # give new names to these columns
        dtype=NAMES,  # enforce string or int types
        **kwargs,
    )


@dataclass
class RemoteZipFile:
    year: int
    
    def __post_init__(self):
        self._size = None 
    
    @property
    def url(self):
        return mk_url(self.year)
    
    def size(self):
        if self._size is None:
           self._size = url_content_length(self.url)
        return self._size  
    
    def download(self, folder=None):        
        return curl(path_zip(self.year), mk_url(self.year))
    
    def is_valid_size(self):
        return self.size() == required_file_size(self.year)


@dataclass
class LocalFile:
    year: int
    folder: Optional[Path] = None
    
    def __post_init__(self):
        if self.folder is None:
           self.folder = default_data_folder()   
    @property 
    def path(self):
        pass # to overload          

    def size(self):
        return self.path.stat().st_size

    def size_mb(self):
        return to_megabytes(self.size())

    def exists(self):
        return self.path.exists()


def to_megabytes(b: int, precision: int = 1):
    return round(b / 2 ** (10 * 2), precision)
    
    
@dataclass    
class LocalZipFile(LocalFile):
   
    @property 
    def path(self):
        return path_zip(self.year, self.folder)
    
    def unpack(self):
        return unzip(self.path)
    
    def contents(self):
        with ZipFile(self.path) as zf:        
            return zf.namelist()

    def is_valid_size(self):
        return self.size() == required_file_size(self.year)

@dataclass
class LocalCSVFile(LocalFile):
    year: int
    folder: Path = default_data_folder()

    @property 
    def path(self):
        return path_csv(self.year, self.folder)

def _download(year, folder=None): 
    remote = RemoteZipFile(year)
    assert remote.is_valid_size()
    print(year, "file size is", remote.size())
    local = LocalZipFile(year)
    if not local.exists() or (local.size() != remote.size()) :
        print("Downloading", year)
        remote.download()
        print("Unpacking", year)
        local.unpack()

def inspect(year):
    return RemoteZipFile(year), LocalCSVFile(year)


import click

@click.group()
def cli():
    """Download 2012-2018 corporate annual financial statements from Rosstat.""" 
    pass

@cli.command()
@click.argument('year')
def url(year: str):
    """Show URL for remote zipfile."""
    year = accept_year(year)
    click.echo(RemoteZipFile(year).url, nl=False)

def accept_year(year):
    year = int(year)
    if year in available_years():
       return year
    else:       
       msg = f"{year} is not a valid YEAR, must be in 2012..2018 range."
       click.echo(msg, err=True)
       raise ValueError(year)
    

@cli.command()
@click.argument('year')
@click.option('--mb', is_flag=True)
def size(year, mb):
    """Show zipfile size in bytes or Mb."""
    year = accept_year(year)
    x = required_file_size(year)
    if mb:
        x = to_megabytes(x)
    click.echo(x)


@cli.command()
@click.argument('year')
def download(year):
    """Download zipfile to local computer."""
    year = accept_year(year)
    remote = RemoteZipFile(year)
    assert remote.is_valid_size()
    click.echo(f"{year} file size is {remote.size()}")
    local = LocalZipFile(year)
    if local.size() != remote.size():
        click.echo("Found local file of wrong size, delete recommended")
        return
    if local.exists():
        click.echo(f"{year} file already exists")
    else:    
        click.echo(f"Downloading {year}")
        remote.download()


@cli.command()
@click.argument('year')
def unpack(year):    
    """Unpack local zipfile as local CSV file."""
    click.echo("Unpacking {year}")
    year = accept_year(year)
    files = LocalZipFile().unpack()
    click.echo("\n".join(files))

    
@cli.command()
@click.argument('year')
@click.option('--csv', 'filetype', flag_value=LocalCSVFile)
@click.option('--zip', 'filetype', flag_value=LocalZipFile)
def path(year, filetype):        
    """Show path to local files."""
    year = accept_year(year)
    if filetype:
      click.echo(filetype(year).path, file=click.get_text_stream('stdout'))
    else:
      click.echo(default_data_folder(), file=click.get_text_stream('stdout'))

def data(year, nrows):
    pass
    
# Ideas:
# one info command for path, size and url
# less boilerlplate with year = accept_year(year)
# restore test option - read from github years 0 and 1
# data year --nrows
# --directory or --dir
# setuptools entry point
# DOI for code
       
if __name__ == "__main__":    
    cli()
