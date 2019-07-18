from pathlib import Path


def whereami(x=__file__):
    return Path(x).parents[0]


def default_data_folder():
    home = Path.home() / ".boo"
    home.mkdir(parents=True, exist_ok=True)
    return home


def get_folder(directory):
    if directory is None:
        return default_data_folder()
    elif directory.is_dir():
        return directory
    else:
        raise FileNotFoundError(directory)


def file(year, tag="", directory=None):
    return get_folder(directory) / f"{year}{tag}.csv"


def raw(year):
    return file(year, "raw")


def processed(year):
    return file(year)