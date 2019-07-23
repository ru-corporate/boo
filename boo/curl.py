"""File download utility."""
import requests
from tqdm import tqdm

from boo.file import panic


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