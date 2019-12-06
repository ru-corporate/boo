"""File download utility."""
from urllib.request import urlopen
import requests
from tqdm import tqdm

from boo.file import panic
from boo.year import make_url

# Note: probably may use pycurl instead


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


def file_length(year: int):
    url = make_url(year)
    with urlopen(url) as f:
        return int(f.info()['Content-Length'])


def file_length_mb(year: int):
    x = file_length(year)
    return int(round(x / (1024 ** 2), 0))
