"""Help message system, deals with state of local CSV files."""

from boo.year import make_url
from boo.path import locate


def raw_state(year):
    r = locate(year).raw
    if r.exists():
        yield f"Raw CSV file downloaded as {r}"
        if r.mb() < 1:
            yield "WARNING: file size too small. Usual size > 500Mb."
    else:
        yield f"Raw CSV file not downloaded. Run `download({year})`."


def processed_state(year):
    p = locate(year).processed
    if p.exists():
        yield f"Processed CSV file is saved as {p}"
        yield f"Use `df=read_dataframe({year})` next."
    else:
        yield f"Final CSV file not built. Run `build({year})`."


def inspect(year: int, directory=None):
    print("URL:", make_url(year))
    for msg in raw_state(year):
        print(msg)
    for msg in processed_state(year):
        print(msg)
