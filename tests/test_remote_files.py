import pytest

from boo.downloader import available_years, file_length


@pytest.mark.skip
def test_rosstat_files_are_available_and_big_in_size():
    for year in available_years():
        assert file_length(year) > 500_000
