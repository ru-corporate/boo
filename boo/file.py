"""CSV file load, read and write operations."""

import csv
import os
import requests
from tqdm import tqdm

import pandas as pd


def panic(path):
    if os.path.exists(path):
        raise FileExistsError("File already exists: %s" % path)


def yield_rows(path,
               enc='windows-1251',
               sep=";"):
    """Emit CSV rows by filename."""
    with open(path, 'r', encoding=enc) as csvfile:
        spamreader = csv.reader(csvfile, delimiter=sep)
        for row in spamreader:
            # filter only non-empty rows, prevent error in `cutf(2016)`
            if row:
                yield row


def save_rows(path,
              stream,
              column_names=None,
              fmt=dict(
                  lineterminator="\n",
                  quoting=csv.QUOTE_MINIMAL),
              # FIXME: mention , ?
              enc='utf-8'):
    panic(path)
    iterable = tqdm(stream, unit=' lines')
    with open(path, 'w', encoding=enc) as file:
        writer = csv.writer(file, **fmt)
        if column_names:
            writer.writerow(column_names)
        writer.writerows(iterable)


def read_df(path, dtypes):
    with open(path, 'r', encoding='utf-8') as f:
        return pd.read_csv(f, dtype=dtypes)
