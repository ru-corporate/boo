from boo.dataframe.canonic import is_numeric_column


def numeric_columns(df):
    return [c for c in df.columns if is_numeric_column(c)]


def n_largest(df, col: str, n: int):
    return sort(df, col).head(n)


def contains(df, text):
    ix = df.title.str.lower().str.contains(text.lower()).fillna(False)
    return df[ix]


def sort(df, col):
    return df.sort_values(col, ascending=False)


def region(df, x: int):
    return df[df.region == x]


def inn(df, x: str):
    return df.loc[str(x), :]


def inns(df, xs):
    xs = list(map(str, xs))
    ix = df.index.isin(xs)
    return df.loc[ix, :]


def random(df, n=1):
    return df.sample(n)


def industry(df, ok1):
    return df[df.ok1 == ok1]


def industry2(df, ok1, ok2):
    return df[(df.ok1 == ok1) & (df.ok2 == ok2)]