from pathlib import Path

from boo.file import curl
from boo.year import make_url


def test_curl():
    curl('temp', make_url(2012), 20)
    p = Path('temp')
    assert p.stat().st_size == 20 * 1024
    p.unlink()
