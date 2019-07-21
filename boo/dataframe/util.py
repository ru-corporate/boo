from boo.dataframe.canonic import is_numeric_column


def mapf(x, *funcs):
    for f in funcs:
        x = f(x)
    return x


def alive(df):
    ix = (df.sales != 0) & (df.cf != 0) & (df.profit_before_tax != 0)
    return df[ix]


def beyond(threshold=0):
    def slicer(df):
        return df[(df.ta > threshold) |
                  (df.sales > threshold) |
                  (df.cf > threshold)]
    return slicer


def n_largest(df, column):
    pass


def numeric_columns(df):
    return [c for c in df.columns if is_numeric_column(c)]


def bln(df):
    M = 1_000_000
    cols = numeric_columns(df)
    df.loc[:, cols] = df.loc[:, cols].divide(M).round(1)
    return df


def contains(df, text):
    ix = df.title.str.lower().str.contains(text.lower()).fillna(False)
    return df[ix]


def sort(df, col):
    return df.sort_values(col, ascending=False)


def region(df, x: int):
    return df[df.region == x]


def inn(df, x: str):
    return df.loc[str(x), :]


def random(df):
    return df.sample(1)


def industry(df, ok1):
    return df[df.ok1 == ok1]


def industry2(df, ok1, ok2):
    return df[(df.ok1 == ok1) & (df.ok2 == ok2)]


def large_companies(df):
    cols = ['region', 'ok1', 'ok2', 'ok3', 'title'] + \
           ['ta', 'cash', 'of', 'sales', 'profit_before_tax', 'cf']
    return mapf(df[cols], alive, bln, beyond(1)) \
        .sort_values("ta", ascending=False) \
        .rename(columns={'profit_before_tax': 'p'})
