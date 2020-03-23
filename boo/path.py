from pathlib import Path

from boo.errors import DirectoryNotFound, NoRawFileError
from boo.helper import as_mb


def default_data_folder() -> Path:
    home = Path.home() / ".boo"
    home.mkdir(exist_ok=True)
    return home


def get_folder(directory=None) -> Path:
    if directory is None:
        return default_data_folder()
    elif Path(directory).is_dir():
        return Path(directory)
    else:
        raise DirectoryNotFound(directory)


def file(year, tag="", directory=None):
    return get_folder(directory) / f"{tag}{year}.csv"


class RawFile:
    encoding = "cp1251"
    
    def __init__(self, year, directory):
        self.path = file(year, "raw", directory)
        self.year = year

    def content(self):
        return self.path.read_text(encoding="cp1251")

    def size(self):
        return self.path.stat().st_size

    def mb(self):
        return as_mb(self.size())

    def folder(self):
        return str(self.path.parent)

    def __str__(self):
        prefix = str(self.path)
        try:
            return prefix + f" ({self.mb()}M)"
        except FileNotFoundError:
            return prefix + " (does not exist)"

    def __repr__(self):
        return repr(self.path)

    def exists(self):
        return self.path.exists()

    def assert_exists(self):
        if not self.exists():
            raise NoRawFileError(self.year)
            
    def print_error(self):
        try:
            self.assert_exists()
        except FileNotFoundError as e:
            print(e)
            