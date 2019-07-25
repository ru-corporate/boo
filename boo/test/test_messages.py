from tempfile import TemporaryDirectory
from boo.messages import inspect

# FIXME: capture stdout


def test_inspect_on_existing_data_is_callable(ARGS_YEAR_0):
    year, folder = ARGS_YEAR_0
    inspect(year, folder)


def test_inspect_on_non_existing_data_is_callable():
    with TemporaryDirectory() as temp_dir:
        inspect(2012, directory=temp_dir)
