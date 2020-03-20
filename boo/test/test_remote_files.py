from boo import years, file_length_mb

def test_rosstat_files_are_available_and_big_in_size():
    for year in years():
        assert file_length_mb(year) > 500
