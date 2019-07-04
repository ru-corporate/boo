"""CSV file load, read and write operations."""

import csv
import os
import requests
from tqdm import tqdm

def panic(path):
    if os.path.exists(path):
        raise FileExistsError("File already exists: %s" % path)    


def curl(path: str, url: str, max_chunk=None):
    panic(path)
    r = requests.get(url, stream=True)
    iterable = tqdm(r.iter_content(chunk_size=1024), unit=' k')
    with open(path, 'wb') as f:
        i = 0
        for chunk in iterable:
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
            i += 1
            if max_chunk and i >= max_chunk:
                break


def yield_rows(path,
               enc='windows-1251',
               sep=";"):
    """Emit CSV rows by filename."""
    with open(path, 'r', encoding=enc) as csvfile:
        spamreader = csv.reader(csvfile, delimiter=sep)
        for row in spamreader:
            yield row


def save_rows(path,
              stream,
              column_names=None,
              fmt=dict(lineterminator="\n", quoting=csv.QUOTE_MINIMAL), #FIXME: mention , ?
              enc='utf-8'):
    panic(path)
    iterable = tqdm(stream, unit=' lines')
    with open(path, 'w', encoding=enc) as file:
        writer = csv.writer(file, **fmt)
        if column_names:
            writer.writerow(column_names)
        writer.writerows(iterable)  


          