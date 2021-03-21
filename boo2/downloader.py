"""Availabale years and URLs for them."""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
from urllib.request import urlopen
from zipfile import ZipFile

import requests
from tqdm import tqdm

# Note: must manually hardcode new timestamps when new version of
# data arrives.


def timestamps(year: int):
    return {
        2012: ("7708234640-", "20200331"),  # different
        2013: ("7708234640-", "20200331"),  # different
        2014: ("7708234640-", "20200327"),  #  similar
        2015: ("7708234640-", "20200327"),  # similar
        2016: ("7708234640-", "20200327"),  # similar
        2017: ("7708234640-", "20200327"),  # similar
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
        2018: 269_452_075,
    }[year]


def size(path):
    return path.stat().st_size


def to_megabytes(b: int, precision: int = 1):
    return round(b / 2 ** (10 * 2), precision)


def is_valid_size(path, year):
    return size(path) == required_file_size(year)


def filename(year):
    _, timestamp = timestamps(year)
    return f"data-{timestamp}-structure-{year}1231"


def csv_filename(year):
    return filename(year) + ".csv"


def zip_filename(year):
    return filename(year) + ".zip"


assert csv_filename(2012) == "data-20200331-structure-20121231.csv"


def mk_url_pure(year):
    mid, _ = timestamps(year)
    return f"https://rosstat.gov.ru/opendata/{mid}bdboo{year}/" + zip_filename(year)


def mk_url(year):
    if year in (0, 1):  # for testing
        return str(year)
    return mk_url_pure(year)


assert (
    mk_url(2018)
    == "https://rosstat.gov.ru/opendata/7708234640-7708234640bdboo2018/data-20200327-structure-20181231.zip"
)


def available_years() -> List[int]:
    """List available years with datasets."""
    return [2012, 2013, 2014, 2015, 2016, 2017, 2018]


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
    """Get size of a remote file at url."""
    with urlopen(url) as f:
        return int(f.info()["Content-Length"])


def file_length(year: int):
    """Get size of a remote url by year."""
    return url_content_length(url=mk_url(year))


def default_data_folder() -> Path:
    home = Path.home() / ".boo"
    home.mkdir(exist_ok=True)
    return home


def unzip(path, folder=None):
    folder = folder if folder else default_data_folder()
    with ZipFile(path) as zf:
        zf.extractall(folder)
        return zf.namelist()


def path_zip(year: int, folder: Optional[Path] = None) -> Path:
    folder = folder if folder else default_data_folder()
    return folder / f"{year}.zip"


def path_csv(year: int, folder: Optional[Path] = None) -> Path:
    folder = folder if folder else default_data_folder()
    return folder / csv_filename(year)


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

    def download(self, destination_folder):
        return curl(path_zip(self.year, destination_folder), self.url)

    def validate_size(self):
        a = self.size()
        b = required_file_size(self.year)
        if a != b:
            raise ValueError(f"Remote file size {a} does not match {b}")

    def is_same_size(self, local_file: Path):
        return size(local_file) == self.size()


def download(year, folder: Optional[str]=None, echo=print):
    folder = Path(folder) if folder else default_data_folder()
    remote_zip = RemoteZipFile(year)
    remote_zip.validate_size()
    echo(year, "remote file size is", remote_zip.size())
    local_zip = path_zip(year, folder)   
    if local_zip.exists() and remote_zip.is_same_size(local_zip):
        echo("File already downloaded:", local_zip)
    else:    
        echo("Downloading for year", year)
        remote_zip.download(folder)
        echo("Downloaded zip file", local_zip)
        echo("Size", size(local_zip))
    return str(local_zip)


def unpack(year, folder: Optional[str]=None, echo=print):  
    folder = Path(folder) if folder else default_data_folder()
    local_zip = path_zip(year, folder)  
    echo("Unpacking local zip file for year", year, "to folder", folder)
    files = unzip(local_zip, folder)    
    if files[0] == csv_filename(year):
       echo("Unpacked", path_csv(year, folder))     
    else:
       echo("Unpacked", " ".join(files))