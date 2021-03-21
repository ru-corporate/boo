from pathlib import Path
from shutil import copyfile
from tempfile import TemporaryDirectory

import pandas as pd
import pytest
from requests.exceptions import ConnectionError

from boo.main import download, inspect, read_dataframe
from boo.path import RawFile

DATA_FOLDER = Path(__file__).parent / "data"


def raw_content():
    return (DATA_FOLDER / "raw0.csv").read_text(encoding="cp1251")


def copy(filename, destination_folder):
    src = DATA_FOLDER / filename
    dst = Path(destination_folder) / filename
    copyfile(src, dst)


def test_download():
    try:
        with TemporaryDirectory() as temp_dir:
            download(year=0, directory=temp_dir)
            r = RawFile(year=0, directory=temp_dir)
            assert r.content() == raw_content()
    # test passes if no internet connection available
    except ConnectionError:
        pass


def test_read_dataframe():
    with TemporaryDirectory() as temp_dir:
        copy("raw0.csv", temp_dir)
        df = read_dataframe(year=0, directory=temp_dir)
        assert isinstance(df, pd.DataFrame)
        assert sum(df.cf) == -7032726


def make_tempfile(folder, filename, content):
    import pathlib

    path = pathlib.Path(folder) / filename
    path.write_text(content, encoding="windows-1251")
    return path


@pytest.fixture
def file_with_missing_value():
    content = """ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ "ВНЕДРЕНЧЕСКИЙ ЦЕНТР ВЕКТОР";00007485;12300;16;62.01;2301091076;384;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;660;484;0;0;953;1478;0;0;281;257;0;0;1894;2219;1895;2219;0;0;0;0;0;0;1702;1953;0;0;0;0;1702;1953;0;0;0;0;0;0;0;0;0;0;0;0;193;267;0;0;0;0;0;0;193;267;1895;2219;5350;4754;3252;2662;2098;2092;0;0;0;0;2098;2092;0;0;0;0;0;0;41;37;59;33;2080;2096;158;159;0;0;0;0;0;0;0;0;1922;1937;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;20190328
    ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ "СУББОТИНА КОВАЛЕНКО";00008237;12300;16;86.23;2308227985;384;1;0;0;0;0;0;0;0;0;102;0;0;0;0;0;0;0;0;0;102;0;0;0;0;0;2020;1659;0;0;274;139;0;0;2294;1798;2396;1798;0;0;0;0;0;0;0;0;0;0;0;0;2334;1432;0;0;0;0;0;0;0;0;0;0;0;0;61;367;0;0;0;0;0;0;61;367;2396;1798;7043;4334;5731;3316;1312;1018;0;0;0;0;1312;1018;0;0;0;0;2;0;0;0;172;109;1138;909;254;128;0;0;0;0;0;0;0;0;884;781;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;20190115
    ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ "УТЕС";00008243;65;16;60.10;2308227978;384;2;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;42;7;0;361;0;10;0;0;42;378;42;378;10;10;0;0;0;0;0;0;0;0;-178;290;-168;300;0;0;0;0;0;0;0;0;0;0;133;45;10;22;0;0;0;0;67;11;210;78;42;378;624;364;263;35;361;329;811;2;0;0;-450;327;0;0;0;0;0;0;0;0;0;0;-450;327;18;23;0;0;0;0;0;0;0;0;-468;304;0;0;0;0;-468;304;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;20190322"""
    content = content.replace(";00008243;", ";;")
    with TemporaryDirectory() as temp_dir:
        make_tempfile(temp_dir, "raw0.csv", content)
        yield 0, temp_dir


def test_read_dataframe_with_missing_values(file_with_missing_value):
    year, folder = file_with_missing_value
    df = read_dataframe(year, folder)
    assert pd.isnull(df.loc["2308227978", "okpo"])


def test_inspect_on_existing_data_is_callable(ARGS_YEAR_0):
    year, folder = ARGS_YEAR_0
    inspect(year, folder)


def test_inspect_on_non_existing_data_is_callable():
    with TemporaryDirectory() as temp_dir:
        inspect(2012, directory=temp_dir)
