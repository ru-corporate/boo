import pandas as pd

from boo.downloader import path_csv
from boo.dataframe import canonic_df
from boo.columns import INDEX, NAMES

def read_intermediate_df(year, directory=None, **user_args):
    """Read intermeiate data for *year* as dataframe.

    You can use read_intermediate_df(year, nrows=100) for small example.

    Returns:
        pandas.DataFrame
    """
    kwargs = dict(
        encoding="windows-1251",
        sep=";",
        header=None,
        usecols=INDEX,  # read only a subset of columns
        names=[x for x in NAMES.keys()],  # give new names to these columns
        dtype=NAMES,  # enforce string or int types
    )
    return pd.read_csv(path_csv(year, directory), **kwargs, **user_args)


def read_dataframe(year: int, directory=None, **kwargs):
    """Read canonic data for *year* as dataframe.

    Returns:
        pandas.DataFrame
    """
    return canonic_df(read_intermediate_df(year, directory, **kwargs))    
