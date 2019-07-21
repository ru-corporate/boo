from pathlib import Path
from dataclasses import dataclass


def whereami(x=__file__):
    return Path(x).parent


def default_data_folder() -> Path:
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


def filesize(path):
    return round(path.stat().st_size / (1024 * 1024.0), 1)


def publish(path) -> str:
    try:
        size = filesize(path)
        return f"{path} ({size}M)"
    except FileNotFoundError:
        return f"{path} does not exist"
