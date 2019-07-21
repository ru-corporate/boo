from tempfile import TemporaryDirectory
from boo.messages import inspect

# FIXME: capture stdout
def test_inspect_on_existing_data(filled_directory):
    inspect(**filled_directory)


def test_inspect_on_non_existing_data():
    with TemporaryDirectory() as temp_dir:
        inspect(2012, directory=temp_dir)
