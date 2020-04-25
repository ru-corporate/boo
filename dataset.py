"""Create processed_2018.csv, processed_2018.xlsx and variables.json stable files."""

import json
import os

import pandas as pd
import boo

# silence chained assignment warnings
pd.options.mode.chained_assignment = None


must_overwrite = True
source_df = boo.read_dataframe(2018)

df = (
    # Assets greater than 1 bln RUB.
    source_df.query("ta > 1_000_000")
    # Has some profit or loss,
    # but not exactly zero thousand RUB,
    # (protects from ghost firms)
    .query("profit_before_tax != 0")
    # Not a financial firm (eg VTB Capital).
    .where(lambda df: ~df.ok1.isin([64, 65]))
    # Gazprom will be on top of list
    .sort_values("ta", ascending=False).dropna()
)

assert "ta_nonfix_fin" in df.columns
assert "receivables" in df.columns

# convert from thousand to billion rub
def numeric_columns(df):
    return [col for col in df.columns if boo.is_numeric_column(col)]


unit = 1_000_000
digits = 3
cols = numeric_columns(df)
df.loc[:, cols] = df.loc[:, cols].divide(unit).round(digits)

# save as CSV and Excel
def locate(filename):
    return os.path.join("assets", filename)


if must_overwrite:
    df.to_csv(locate("processed_2018.csv"))
    df.to_excel(locate("processed_2018.xlsx"))

variables = {col: boo.whatis(col) for col in df.columns}
assert variables["receivables"] == "Дебиторская задолженность"

with open(locate("variables.json"), "w") as f:
    json.dump(variables, f, ensure_ascii=False)

print("Done")
