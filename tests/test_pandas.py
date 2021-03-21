import pandas as pd

# https://github.com/pandas-dev/pandas/issues/38844
def test_will_fail_before_version_1_3():
    df = pd.DataFrame([{'a':1.2},{'a':2.5}])
    df = df.convert_dtypes()
    df['a'] = df['a'].round()