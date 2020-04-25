from boo.curl import file_length_mb
from boo.year import available_years


def test_rosstat_files_are_available_and_big_in_size():
    for year in available_years():
        assert file_length_mb(year) > 500
