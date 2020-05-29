"""Custom error types."""

from typing import List


class UnclassifiableCodeError(ValueError):
    pass


def commas(xs):
    return ", ".join(map(str, xs))


class WrongYearError(ValueError):
    def __init__(self, year: int, allowed: List[int]):
        super().__init__(
            "Year not supported.\n"
            f"Provided year: {year}.\n"
            f"Allowed years: {commas(allowed)}.\n"
            "Update timestamp definitions in year.py if necessary."
        )


class DirectoryNotFound(FileNotFoundError):
    pass


class NoRawFileError(FileNotFoundError):
    def __init__(self, year):
        super().__init__(
            f"Raw CSV file not downloaded for {year}. " f"Try `boo.download({year})`."
        )
