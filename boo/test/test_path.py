from boo.path import locate, Raw, Processed

import pytest
from shutil import copyfile
from pathlib import Path
from tempfile import TemporaryDirectory

DATA_FOLDER = Path(__file__).parent / "data"

def raw_content():
    return (DATA_FOLDER / "raw0.csv").read_text(encoding="cp1251")


def processed_content():
    return (DATA_FOLDER / "0.csv").read_text(encoding="utf-8")


def size(path):
    return path.stat().st_size 


@pytest.fixture
def size_raw():
    return size(DATA_FOLDER / "raw0.csv")


@pytest.fixture
def size_processed():
    return size(DATA_FOLDER / "0.csv")


def copy(filename, destination_folder):
    src = DATA_FOLDER / filename
    dst = Path(destination_folder) / filename
    copyfile(src, dst)
    

def test_locate():
    loc = locate(0)
    assert isinstance(loc.raw, Raw)
    assert isinstance(loc.processed, Processed)

@pytest.mark.xfail    
def test_size():
    with TemporaryDirectory() as temp_dir:
        copy("raw0.csv", temp_dir)
        copy("0.csv", temp_dir)
        raise ValueError(temp_dir)
        kwargs = dict(year=0, directory=temp_dir)
        r = Raw(*kwargs)
        assert r.size() == 11490    
        p = Processed(*kwargs)
        assert p.size() == 5531

@pytest.mark.xfail
def test_content(raw_content, processed_content):
    with TemporaryDirectory() as temp_dir:
        copy("raw0.csv", temp_dir)
        copy("0.csv", temp_dir)
        kwargs = dict(year=0, directory=temp_dir)
        assert Raw(*kwargs).content() == raw_content
        assert Processed(*kwargs).content() == processed_content
