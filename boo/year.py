"""Availabale years and URLs for them."""
from boo.errors import WrongYearError

from typing import List

# Note: must manually hardcode new timestamps when new version of data arrives.

TIMESTAMPS = {
    2012: 20190329,
    2013: 20190411,
    2014: 20190411,
    2015: 20190411,
    2016: 20190411,
    2017: 20190423,
    2018: 20191029,
}


def available_years() -> List[int]:
    """List available years with datasets."""
    return list(TIMESTAMPS.keys())


def get_timestamp(year: int, timestamps=TIMESTAMPS):
    try:
        return timestamps[year]
    except KeyError:
        raise WrongYearError(year, allowed=available_years())


def rosstat_url(year: int, timestamps=TIMESTAMPS):
    """
    Construct URL similar to
    http://www.gks.ru/opendata/storage/7708234640-bdboo2012/data-20181029t000000-structure-20121231t000000.csv
    using timestamps.
    """
    timestamp = get_timestamp(year)
    return (
        "http://www.gks.ru/opendata/storage/"
        f"7708234640-bdboo{year}/"
        f"data-{timestamp}t000000-structure-"
        f"{year}1231t000000.csv"
    )


def testing_url(year: int):
    return (
        "https://raw.githubusercontent.com/"
        "ru-corporate/boo/master/assets/"
        f"sample{year}.txt"
    )


def make_url(year: int) -> str:
    if year in [0, 1]:  # allowed year numbers for testing
        return testing_url(year)
    return rosstat_url(year)
