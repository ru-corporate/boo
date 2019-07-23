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
    
    
class Test_filled_directory(object):
    def setup_method(self):
        self.temp_dir = TemporaryDirectory()
        copy("raw0.csv", self.temp_dir.name)
        copy("0.csv", self.temp_dir.name)
        self.kwargs = dict(year=0, directory=self.temp_dir)
        
    def teardown_method(self):
        self.temp_dir.cleanup()