import pytest
from pathlib import Path 

DATA_FOLDER = Path(__file__).parent / "data"

@pytest.fixture
def raw_content():
    return (DATA_FOLDER / "raw0.csv").read_text()


@pytest.fixture    
def processed_content():
    return (DATA_FOLDER / "0.csv").read_text()


@pytest.fixture
def filled_directory():
    yield dict(year=0, directory=str(DATA_FOLDER))
