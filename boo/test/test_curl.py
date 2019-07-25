import pytest
from pathlib import Path
from tempfile import NamedTemporaryFile

from requests.exceptions import ConnectionError

from boo.curl import curl
from boo.year import make_url

# FIXME: ask at SO

@pytest.fixture
def tempname():
    with NamedTemporaryFile() as f:
        name = f.name
    yield name
    if Path(name).exists():
        Path(name).unlink()

# FIXME: valid year fixture

def test_curl(tempname):
    n = 3
    curl(path=tempname, url=make_url(2012), max_chunk=n)
    assert Path(tempname).stat().st_size == n * 1024