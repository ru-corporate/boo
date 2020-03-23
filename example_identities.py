# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 09:38:07 2020

@author: Евгений
"""

import numpy as np
import pandas as pd

import boo

pd.options.mode.chained_assignment = None

try:
    df_full
except NameError:
    print("Reading the data file...")
    df_full = boo.read_dataframe(2012)

# Identities:
#   ta = tp
#   ta_fix + ta_nonfix = ta
#   tp = tp_capital + tp_long + tp_short
#
#   cf_oper + cf_inv + cf_fin = cf

df = df_full
textual = [
    "title",
    "org",
    "okpo",
    "okopf",
    "okfs",
    "okved",
    "unit",
    "ok1",
    "ok2",
    "ok3",
    "region",
]
numeric = [col for col in df.columns if col not in textual]
df["title"] = df.title.apply(lambda x: x[0:20])
df.loc[:, numeric] = df.loc[:, numeric].divide(1000).round(1)

# zf = df[df.ta !=0][['title','ta','tp']]
# zf['delta'] = zf.tp-zf.ta
# zf['rel'] = (zf.delta).abs() / zf.ta
# zf.sort_values('delta').tail(10)
# zf.sort_values('delta').head(10)

# d = lookup_df.delta.abs()
# d = d[(d>0.1) & (d<5)]
# d.hist()

ix = df.ta != 0
ix = ix & ((df.ta - df.tp).abs() < 3)
df = df[ix]

df["cf_diff"] = (df.cf_oper + df.cf_inv + df.cf_fin - df.cf).abs()
df[df.cf_diff > 0].sort_values("cf_diff", ascending=False)[
    ["title", "cf", "cf_oper", "cf_inv", "cf_fin"]
]
