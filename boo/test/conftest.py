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


@pytest.fixture
def SIZE_RAW():
    return size(DATA_FOLDER / "raw0.csv")


@pytest.fixture
def SIZE_PROCESSED():
    return size(DATA_FOLDER / "0.csv")


@pytest.fixture
def directory_with_files(tmpdir):
    copy("raw0.csv", tmpdir)
    copy("0.csv", tmpdir)
    return str(tmpdir)


@pytest.fixture
def ARGS_YEAR_0(directory_with_files):
    return 0, str(directory_with_files)
