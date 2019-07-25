import pytest
import os
from pathlib import Path

from boo.path import locate, Raw, Processed, get_folder


def test_get_folder(ARGS_YEAR_0):
    _, dir0 = ARGS_YEAR_0
    f = get_folder(directory=dir0)
    assert isinstance(f, Path)
    assert str(f) == dir0


def test_get_folder_on_none():
    f = get_folder(directory=None)
    assert f.is_dir()
    path, file = os.path.split(f)
    assert file == ".boo"


def test_size_raw(ARGS_YEAR_0, SIZE_RAW):
    year, folder = ARGS_YEAR_0
    r = Raw(year, folder)
    assert r.size() == SIZE_RAW > 0  # 11490


def test_size_proc(ARGS_YEAR_0, SIZE_PROCESSED):
    year, folder = ARGS_YEAR_0
    p = Processed(year, folder)
    assert p.size() == SIZE_PROCESSED > 0  # 5531


def test_locate():
    loc = locate(0)
    assert isinstance(loc.raw, Raw)
    assert isinstance(loc.processed, Processed)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
