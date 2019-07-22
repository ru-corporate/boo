import pytest
from pathlib import Path
from tempfile import TemporaryDirectory


DATA_FOLDER = Path(__file__).parent / "data"

@pytest.fixture
def directory_after_download_args():
    with TemporaryDirectory() as temp_dir:
        p = (Path(temp_dir) / "raw0.csv")
        p.write_text(raw_content())
        yield (0, temp_dir)

@pytest.fixture
def filled_directory():
    return DATA_FOLDER 
    

@pytest.fixture
def raw_content():
    return (DATA_FOLDER / "raw0.csv").read_text()


@pytest.fixture
def processed_content():
    return (DATA_FOLDER / "0.csv").read_text(encoding="utf-8")


@pytest.fixture
def filled_directory_args():
    yield dict(year=0, directory=str(DATA_FOLDER))
