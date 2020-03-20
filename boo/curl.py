"""File download utility."""
from urllib.request import urlopen

import requests
from tqdm import tqdm

from boo.year import make_url
from boo.helper import as_mb


def curl(path: str, url: str, max_chunk=None):
    r = requests.get(url, stream=True)
    iterable = tqdm(r.iter_content(chunk_size=1024), unit=" k")
    with open(path, "wb") as f:
        i = 0
        for chunk in iterable:
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
            i += 1
            if max_chunk and i >= max_chunk:
                break


def url_content_length(url: str) -> int:
    with urlopen(url) as f:
        return int(f.info()["Content-Length"])


def file_length(year: int):
    return url_content_length(url=make_url(year))


def file_length_mb(year: int):
    return as_mb(file_length(year))
