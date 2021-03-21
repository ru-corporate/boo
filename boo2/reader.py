from columns import INDEX, NAMES
import pandas as pd
from downloader import path_csv


def read_intermediate_df(year, directory=None, **user_args):
    # can use read_intermediate_df(year, nrows=100) for small example

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
