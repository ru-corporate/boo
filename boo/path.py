from pathlib import Path
from dataclasses import dataclass


def whereami(x=__file__):
    return Path(x).parents[0]


def default_data_folder():
    home = Path.home() / ".boo"
    home.mkdir(parents=True, exist_ok=True)
    return home


def get_folder(directory=None) -> Path:    
    if directory is None:
        return default_data_folder()
    elif Path(directory).is_dir():
        return Path(directory)
    else:
        raise FileNotFoundError(directory)


def file(year, tag="", directory=None):
    return get_folder(directory) / f"{tag}{year}.csv"


@dataclass
class Files:
    raw: Path
    processed: Path


def locate(year, directory=None):
    return Files(raw=file(year, "raw", directory),
                 processed=file(year, "", directory)) 
