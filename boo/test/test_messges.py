from tempfile import TemporaryDirectory
from requests.exceptions import ConnectionError
from boo.messages import inspect
from boo.main import download, build

# FIXME: capture stdout
# FIXME: make a fixture for index 0 build, sharable for the suite, download once
def test_inspect_on_existing_data():
    try:
        with TemporaryDirectory() as temp_dir:
            download(year=0, force=True, directory=temp_dir)
            build(year=0, force=True, directory=temp_dir)
            inspect(year=0, directory=temp_dir)
    except ConnectionError:
        pass


def test_inspect_on_non_existing_data():
    with TemporaryDirectory() as temp_dir:
        inspect(2012, directory=temp_dir)
