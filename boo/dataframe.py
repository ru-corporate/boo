"""Преобразовать данные:

- Привести все строки к одинаковым единицам измерения (тыс. руб.)
- Убрать отдельные неиспользуемые колонки
- Новые колонки:
    * короткое название компании
    * код ОКВЭД разбить на три уровня
    * определить регион по ИНН
"""
from .columns import SHORT_COLUMNS
import numpy

QUOTE_CHAR = '"'
EMPTY = int(0)
NUMERIC_COLUMNS = SHORT_COLUMNS.numeric


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
    del df['name']
    return df


UNIT_TO_FUNC = {"385": lambda x: x.multiply(1000),  # mln_to_thousand
                "384": lambda x: x.divide(1000).round(0).astype(int)}  # rub_to_thousand


def adjust_rub(df, mapper=UNIT_TO_FUNC, cols=NUMERIC_COLUMNS):
    for unit, func in mapper.items():
        rows = (df.unit == unit)
        df.loc[rows, cols] = df[rows][cols].apply(func)
        df.loc[rows, "unit"] = "384"
    del df['unit']
    return df


def okved3(code_string: str):
    """Get 3 levels of OKVED codes from *code_string*."""
    codes = [int(x) for x in code_string.split(".")]
    if len(codes) > 3:
        raise ValueError(code_string)
    return codes + [0] * (3 - len(codes))

# MAYBE: add descriptions
# def new_text_field_name(varname: str):
#    okv = lambda text: f"Код ОКВЭД {text} уровня"
#    return {'ok1': okv("первого"),
#            'ok2': okv("второго"),
#            'ok3': okv("третьего"),
#            'org': "Тип юридического лица (часть наименования организации)",
#            'title': "Короткое название организации",
#            'region': "Код региона по ИНН"}.get(varname)


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


def canonic_df(df):
    for f in [adjust_rub, add_okved_subcode, add_region, add_title]:
        df = f(df)
    return df.loc[:, canonic_columns()]


def get_numeric_columns(numeric=SHORT_COLUMNS.numeric):
    return numeric + ['ok1', 'ok2', 'ok3', 'region']


def canonic_dtypes(numeric=SHORT_COLUMNS.numeric):
    numerics = get_numeric_columns()

    def switch(col):
        return numpy.int64 if (col in numerics) else str
    return {col: switch(col) for col in canonic_columns()}


def canonic_columns(numeric=SHORT_COLUMNS.numeric):
    return (['title', 'org', 'okpo', 'okopf', 'okfs', 'okved', 'inn'] +
            ['ok1', 'ok2', 'ok3', 'region'] +
            numeric)

# MAYBE: make 50 + 50 + 1000 example


if __name__ == "__main__":
    from boo import read_intermediate_df as read
    df = canonic_df(read(2012))
