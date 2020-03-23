import numpy as np
import pandas as pd 
from matplotlib import pyplot as plt

import boo

# Silence chained assignment warnings
pd.options.mode.chained_assignment = None

cols = "ok1 title ta sales profit_before_tax".split()

def sort(df, col):
    return df.sort_values(col, ascending=False)
 

def matrix(df, n=100):
    import missingno as msno
    cols = [col for col in df.columns if not col.endswith("lag")]
    return msno.matrix(df.sample(n)[cols].replace(0,np.nan))


def add_ratios(df):
   df["profit_to_sales"] = (df.profit_before_tax / df.sales).round(2)
   df["sales_to_assets"] = (df.sales / df.ta).round(2)
   return df


def numeric_columns(df):
    return [col for col in df.columns if boo.is_numeric_column(col)]

# NEXT: download data

year = 2018
url = "https://boodata.s3.eu-central-1.amazonaws.com/data-20191029t000000-structure-20181231t000000.csv"
boo.download_direct(url, year, force=False)
print("Reading dataframe...")
source_df = boo.read_dataframe(year, nrows=300_000)

# CHECKPOINT: we have dataset loaded in *source_df*

# DISCUSS: why some columns are missing and some are always there
print(len(source_df))
matrix(sort(source_df,'ta'))

# NEXT: prepare smaller file and save as CSV and Excel

# Total assets greater than 1 bln rub and has profit or loss
df = (source_df.query("ta > 1_000_000")
               .query('profit_before_tax != 0')
               .where(lambda df: ~df.ok1.isin([64, 65]))
               .sort_values('ta', ascending=False) 
               .dropna()
)
unit =  1_000_000
df.loc[:, numeric_columns] = df.loc[:, numeric_columns].divide(unit).round(1)

print(len(df))
matrix(sort(df,'ta'))
df.to_csv('processed_2018.csv')
df.to_excel('processed_2018.xlsx')

