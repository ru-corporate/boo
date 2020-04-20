import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

import boo


def sort(df, col):
    return df.sort_values(col, ascending=False)


def unlag(df):
    return [col for col in df.columns if not col.endswith("lag")]


def matrix(df, n=100):
    import missingno as msno

    cols = unlag(df)
    return msno.matrix(df.sample(n)[cols].replace(0, np.nan))


def numeric_columns(df):
    return [col for col in df.columns if boo.is_numeric_column(col)]


# Download Rosstat data
year = 2018
url = "https://boodata.s3.eu-central-1.amazonaws.com/data-20191029t000000-structure-20181231t000000.csv"
boo.download_direct(url, year, force=False)
#    N = 300_000
#    source_df = boo.read_dataframe(year, nrows=N)
source_df = boo.read_dataframe(year)

# 1. Prepare smaller file
df = (
    source_df.query("ta > 1_000_000")  # assets greater than 1 bln ru
    .query("profit_before_tax != 0")  # has some profit or loss, but not 0 tRUB
    .where(lambda df: ~df.ok1.isin([64, 65]))  # not a financial firm
    .sort_values("ta", ascending=False)
    .dropna()
)

# 2. Convert from thousand to bln rub
# silence chained assignment warnings
pd.options.mode.chained_assignment = None
unit = 1_000_000
digits = 2
fc = numeric_columns(df)
df.loc[:, fc] = df.loc[:, fc].divide(unit).round(digits)

# Save as CSV and Excel
must_overwrite = False
if must_overwrite:
    df.to_csv("processed_2018.csv")
    df.to_excel("processed_2018.xlsx")

# To dicuss: why some columns are missing and some are always there
print(len(source_df))
matrix(sort(source_df, "ta"))

print(len(df))
matrix(sort(df, "ta"))
