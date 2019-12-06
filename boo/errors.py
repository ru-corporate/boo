class UnclassifiableCodeError(ValueError):
    pass


class WrongYearError(ValueError):
    def __init__(self, year):
        super().__init__(f"Year not supported: {year}.\n"
                         "Try year starting 2012 up to recent year.\n"
                         "Update definitions in year.py if necessary")


class DirectoryNotFound(FileNotFoundError):
    pass


class NoRawFileError(FileNotFoundError):
    def __init__(self, year):
        super().__init__(
            f"Raw CSV file not downloaded for {year}. "
            f"Try `boo.download({year})`.")


class NoProcessedFileError(FileNotFoundError):
    def __init__(self, year):
        super().__init__(
            f"Final CSV file not built for {year}. "
            f"Try `boo.build({year})`."
        )
