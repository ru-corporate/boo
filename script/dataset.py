"""Create processed_2018.csv, processed_2018.xlsx, mos.zip and variables.json stable files."""

import json
import os

import pandas as pd

import boo

# silence chained assignment warnings
pd.options.mode.chained_assignment = None


def numeric_columns(df):
    return [col for col in df.columns if boo.is_numeric_column(col)]


def in_region(df, codes):
    return df[df.region.isin(codes)]


def change_unit(df, divide_by=1_000_000, digits=3):
    # convert from thousand to billion rub and round to 3 digits
    cols = numeric_columns(df)
    zf = df.copy()
    zf.loc[:, cols] = zf.loc[:, cols].divide(divide_by).round(digits)
    return zf


# save as CSV and Excel
def locate(filename):
    return os.path.join("assets", filename)


if __name__ == "__main__":
    must_overwrite = True

    boo.download(2018)
    source_df = boo.read_dataframe(2018)
    print("Finished reading file, querying...")

    # Has some profit or loss, but not exactly zero thousand RUB,
    # (protects from ghost firms)
    ix = source_df.profit_before_tax != 0

    # Not a financial firm
    ix = ix & (~source_df.ok1.isin([64, 65]))

    # Gazprom will be on top of list
    df = source_df[ix].sort_values("ta", ascending=False).dropna()

    if must_overwrite:
        print("Saving files...")
        df1 = change_unit(df, divide_by=1_000_000, digits=3).query("ta>1")
        df1.to_csv(locate("processed_2018.csv"))
        df1.to_excel(locate("processed_2018.xlsx"))
        df2 = in_region(df, [97, 99, 77, 50])
        df2.to_csv(locate("mos.zip"))

    variables = {col: boo.whatis(col) for col in df.columns}

    with open(locate("variables.json"), "w") as f:
        json.dump(variables, f, ensure_ascii=False)

    print("Done")
