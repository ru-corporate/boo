import pytest
from pathlib import Path
from tempfile import NamedTemporaryFile

from requests.exceptions import ConnectionError

from boo.curl import curl
from boo.year import make_url


@pytest.fixture
def tempname():
    with NamedTemporaryFile() as f:
        name = f.name
    yield name
    if Path(name).exists():
        Path(name).unlink()


def test_curl(tempname):
    try:
        n = 3
        curl(path=tempname, url=make_url(2012), max_chunk=n)
        assert Path(tempname).stat().st_size == n * 1024
    # test passes if no internet connection available
    except ConnectionError:
        pass
