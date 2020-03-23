import pytest
import os
from pathlib import Path

from boo.path import RawFile, get_folder


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
    r = RawFile(year, folder)
    assert r.size() == SIZE_RAW > 0  # 11490


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
