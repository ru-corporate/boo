from boo.path import locate, Raw, Processed

def test_locate():
    loc = locate(0)
    assert isinstance(loc.raw, Raw)
    assert isinstance(loc.processed, Processed)

    
def test_raw_size(filled_directory_args):
    r = Raw(**filled_directory_args)
    assert r.size() == 11490

    
def test_proc_size(filled_directory_args):
    p = Processed(**filled_directory_args)
    assert p.size() == 5531


def test_raw_content(filled_directory_args, raw_content):
    assert Raw(**filled_directory_args).content() == raw_content


def test_proc_content(filled_directory_args, processed_content):
    assert Processed(**filled_directory_args).content() == processed_content

if __name__ == "__main__":    
    import conftest
    year, tmp_dir = next(conftest.filled_directory_args())
    print(Raw(year, tmp_dir).content())     
        