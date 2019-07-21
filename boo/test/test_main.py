import pytest
import pandas as pd
from boo.main import read_dataframe

#    try:
#        with TemporaryDirectory() as temp_dir:
#            kwargs = dict(year=0, force=True, directory=temp_dir)
#            download(**kwargs)
#            build(**kwargs)
#            yield dict(year=0, directory=temp_dir)
#    except ConnectionError:
#         pass

def test_download(filled_directory):
    pass

def test_build(filled_directory):
    pass

def test_read_dataframe(filled_directory):
    df = read_dataframe(**filled_directory)
    assert isinstance(df, pd.DataFrame)
    assert sum(df.cf) == -7032726

if __name__ == "__main__":
    pytest.main([__file__])