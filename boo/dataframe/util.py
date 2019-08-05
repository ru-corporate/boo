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


def industry(df, ok1, ok2=None):
    if ok2 is None:
        return df[df.ok1 == ok1]
    else:
        return df[(df.ok1 == ok1) & (df.ok2 == ok2)]
