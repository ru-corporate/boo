# orphan code

from boo.path import raw, processed, canonic
from boo.dataframe import canonic_df, canonic_dtypes


# FIXME: may delete this
def save_canonic_df(year: int, force=False):
    dst = canonic(year)
    preclean(dst, force)
    print(f"Reading intermediate dataframe for {year}...")
    df = make_canonic_df(year) 
    print(f"Created final dataframe for {year}")
    print(f"Saving to {dst}...")
    write_df(df, dst)
    print("Done")
    return dst


def read_canonic_df(year):
    src = canonic(year)
    return read_df(src, dtypes=canonic_dtypes())


# FIXME: may delete this
def put(year: int):
    return make_canonic_df(year, force=False)


def putf(year: int):
    return make_canonic_df(year, force=True)


def write_df(df, path):
    df.to_csv(
        path,
        index=False,
        header=True,
        chunksize=100_000,
        encoding='utf-8')
