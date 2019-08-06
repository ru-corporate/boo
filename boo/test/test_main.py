from shutil import copyfile
from pathlib import Path
from tempfile import TemporaryDirectory

from requests.exceptions import ConnectionError
import pandas as pd

from boo.main import download, build, read_dataframe, inspect
from boo.path import Processed, Raw


DATA_FOLDER = Path(__file__).parent / "data"


def raw_content():
    return (DATA_FOLDER / "raw0.csv").read_text(encoding="cp1251")


def processed_content():
    return (DATA_FOLDER / "0.csv").read_text(encoding="utf-8")


def copy(filename, destination_folder):
    src = DATA_FOLDER / filename
    dst = Path(destination_folder) / filename
    copyfile(src, dst)


def test_download():
    try:
        with TemporaryDirectory() as temp_dir:
            download(year=0, directory=temp_dir)
            r = Raw(year=0, directory=temp_dir)
            assert r.content() == raw_content()
    # test passes if no internet connection available
    except ConnectionError:
        pass


def test_build():
    with TemporaryDirectory() as temp_dir:
        copy("raw0.csv", temp_dir)
        build(year=0, directory=temp_dir)
        p = Processed(year=0, directory=temp_dir)
        assert p.content() == processed_content()


def test_read_dataframe():
    with TemporaryDirectory() as temp_dir:
        copy("0.csv", temp_dir)
        df = read_dataframe(year=0, directory=temp_dir)
        assert isinstance(df, pd.DataFrame)
        assert sum(df.cf) == -7032726

def test_inspect_on_existing_data_is_callable(ARGS_YEAR_0):
    year, folder = ARGS_YEAR_0
    inspect(year, folder)


def test_inspect_on_non_existing_data_is_callable():
    with TemporaryDirectory() as temp_dir:
        inspect(2012, directory=temp_dir)

