"""Availabale years and URLs for them."""
from boo.errors import WrongYearError

from typing import List

# Note: must manually hardcode new timestamps when new version of data arrives.


def mk_url(year, timestamp):
    return (
        "https://rosstat.gov.ru/opendata/"
        f"7708234640-bdboo{year}/"
        f"data-{timestamp}-structure-{year}1231.zip"
    )


URLs = {
    2012: mk_url(2012, "20200331"),
    2013: mk_url(2013, "20200331"),
    2014: mk_url(2014, "20200327"),
    2015: mk_url(2015, "20200327"),
    2016: mk_url(2016, "20200327"),
    2017: mk_url(2017, "20200327"),
    2018: "https://rosstat.gov.ru/opendata/7708234640-7708234640bdboo2018/data-20200327-structure-20181231.zip",
}


def available_years() -> List[int]:
    """List available years with datasets."""
    return list(URLs.keys())


def rosstat_url(year: int, urls=URLs):
    try:
        return URLs[year]
    except KeyError:
        raise WrongYearError(year)


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
