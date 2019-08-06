import os
from pathlib import Path
from dataclasses import dataclass


def whereami(x=__file__):
    return Path(x).parent


def default_data_folder() -> Path:
    home = Path(os.path.expanduser(".boo"))
    home.mkdir(exist_ok=True)
    return home

# class DirectoryNotFound(FileNotFoundError):
#    pass


def get_folder(directory=None) -> Path:
    if directory is None:
        return default_data_folder()
    elif Path(directory).is_dir():
        return Path(directory)
    else:
        raise FileNotFoundError(directory)


def file(year, tag="", directory=None):
    return get_folder(directory) / f"{tag}{year}.csv"


class File():
    def __init__(self, year, tag, directory):
        self.path = file(year, tag, directory)
        self.year = year

    def size(self):
        return self.path.stat().st_size

    def mb(self):
        return round(self.size() / (1024 * 1024), 1)

    def exists(self):
        return self.path.exists()

    def __str__(self):
        try:
            return f"{self.path} ({self.mb()}M)"
        except FileNotFoundError:
            return f"{self.path} (does not exist)"

    def __repr__(self):
        return repr(self.path)


class Raw(File):
    def __init__(self, year, directory):
        super().__init__(year, "raw", directory)

    def content(self):
        return self.path.read_text(encoding="cp1251")

    def state(self):
        if self.path.exists():
            yield f"Raw CSV file downloaded as {self}"
            if self.mb() < 1:
                yield "WARNING: file size too small. Usual size is larger than 500Mb."
        else:
            yield f"Raw CSV file not downloaded. Run `download({self.year})`."


class Processed(File):
    def __init__(self, year, directory):
        super().__init__(year, "", directory)

    def content(self):
        return self.path.read_text(encoding="utf-8")

    def state(self):
        if self.path.exists():
            yield f"Processed CSV file is saved as {self}"
            yield f"Use `df=read_dataframe({self.year})` next."
        else:
            yield f"Final CSV file not built. Run `build({self.year})`."


@dataclass
class Files:
    raw: Raw
    processed: Processed


def locate(year, directory=None):
    return Files(raw=Raw(year, directory),
                 processed=Processed(year, directory))
