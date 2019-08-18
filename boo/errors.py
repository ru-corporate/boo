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