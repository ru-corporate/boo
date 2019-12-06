import pytest
from pathlib import Path
from tempfile import NamedTemporaryFile

from boo.curl import curl, file_length, file_length_mb
from boo.year import make_url


@pytest.fixture
def tempname():  # FIXME: maybe there is a shorter way to make a tempname
    with NamedTemporaryFile() as f:
        name = f.name
    yield name
    if Path(name).exists():
        Path(name).unlink()


def test_curl(tempname):
    n = 3
    curl(path=tempname, url=make_url(2012), max_chunk=n)
    assert Path(tempname).stat().st_size == n * 1024


def test_file_length():
    assert file_length(0) == 11490


def test_file_length_mb():
    assert file_length_mb(0) == 0
