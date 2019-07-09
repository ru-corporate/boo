"""Преобразовать данные внтури датафрейма:

- Привести все строки к одинаковым единицам измерения (тыс. руб.)
- Убрать  неиспользуемые колонки (date_revised, report_type)
- Новые колонки:
    * короткое название компании
    * три уровня кода ОКВЭД
    * регион (по ИНН)

"""
import numpy
from boo.columns import SHORT_COLUMNS

QUOTE_CHAR = '"'
EMPTY = int(0)
NUMERIC_COLUMNS = SHORT_COLUMNS.numeric


# FIXME: very slow code, even on small data
def adjust_rub(df, cols=NUMERIC_COLUMNS):
    rows = (df.unit == "385")
    df.loc[rows, cols] = df.loc[rows, cols].multiply(1000)
    df.loc[rows, "unit"] = "384"
    rows = (df.unit == "383")
    df.loc[rows, cols] = df.loc[rows, cols].divide(1000).round(0).astype(int)
    df.loc[rows, "unit"] = "384"
    return df


def dequote(name: str):
    """Split company *name* to organisation and title."""
    # Warning: will not work well on company names with more than 4 quotechars
    parts = name.split(QUOTE_CHAR)
    org = parts[0].strip()
    cnt = name.count(QUOTE_CHAR)
    if cnt == 2:
        title = parts[1].strip()
    elif cnt > 2:
        title = QUOTE_CHAR.join(parts[1:])
    else:
        title = name
    return org, title.strip()


def add_title(df):
    s = df.name.apply(dequote)
    df['org'] = s.apply(lambda x: x[0])
    df['title'] = s.apply(lambda x: x[1])
    return df


def okved3(code_string: str):
    """Get 3 levels of OKVED codes from *code_string*."""
    codes = [int(x) for x in code_string.split(".")]
    if len(codes) > 3:
        raise ValueError(code_string)
    return codes + [0] * (3 - len(codes))


def add_okved_subcode(df):
    df['ok1'], df['ok2'], df['ok3'] = zip(*df.okved.apply(okved3))
    return df


def fst(x):
    try:
        return int(x[0:2])
    except TypeError:
        return 0


def add_region(df):
    df['region'] = df.inn.apply(fst)
    return df


def cut_stale_rows(df):
    return df[~((df.ta == 0) & (df.ta_lag == 0))]


def canonic_df(df):
    for f in [adjust_rub, add_okved_subcode, add_region, add_title]:
        df = f(df)
    return df.loc[:, canonic_columns()]


def canonic_columns(numeric=SHORT_COLUMNS.numeric):
    return (['title', 'org', 'okpo', 'okopf', 'okfs', 'okved', 'inn'] +
            ['unit'] +
            ['ok1', 'ok2', 'ok3', 'region'] +
            numeric)


def random(df):
    return df[['inn', 'title', 'ta', 'sales', 'profit_before_tax', 'cf']]\
        .sample(1).transpose()


def get_numeric_columns(numeric=SHORT_COLUMNS.numeric):
    return numeric + ['ok1', 'ok2', 'ok3', 'region']


def canonic_dtypes(numeric=SHORT_COLUMNS.numeric):
    numerics = get_numeric_columns()

    def switch(col):
        return numpy.int64 if (col in numerics) else str
    return {col: switch(col) for col in canonic_columns()}
