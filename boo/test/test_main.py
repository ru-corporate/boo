from tempfile import TemporaryDirectory
from requests.exceptions import ConnectionError
import pandas as pd
from boo.main import download, build, read_dataframe


def test_pipeline():
    try:
        with TemporaryDirectory() as temp_dir:
            download(year=0, force=True, directory=temp_dir)
            build(year=0, force=True, directory=temp_dir)
            df = read_dataframe(year=0, directory=temp_dir)
            assert isinstance(df, pd.DataFrame)
            assert sum(df.cf) == -7032726
    except ConnectionError:
        pass
