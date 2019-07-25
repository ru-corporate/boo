import pytest

from pathlib import Path


@pytest.fixture
def tempdir(tmpdir):
    return Path(tmpdir)


def test_dir(tempdir):
    assert tempdir.exists()


if __name__ == "__main__":
    pytest.main([__file__])
