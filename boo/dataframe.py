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

def replace_names(title: str):
    return title \
        .replace("ПУБЛИЧНОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО", "ПАО") \
        .replace("ОТКРЫТОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО", "ОАО") \
        .replace("НЕФТЕПЕРЕРАБАТЫВАЮЩИЙ ЗАВОД", "НПЗ")\
        .replace("ГЕНЕРИРУЮЩАЯ КОМПАНИЯ ОПТОВОГО РЫНКА ЭЛЕКТРОЭНЕРГИИ", "ОГК")

def add_title(df):
    s = df.name.apply(dequote)
    df['org'] = s.apply(lambda x: x[0])
    df['title'] = s.apply(lambda x: replace_names(x[1]))
    return df

# FIXME: use this on longer names
#def deep_dequote(title):
#    return dequote(str(title))[1]    

SHORT_NAMES_BY_INN = {
    '2460066195': "РусГидро",
    '4716016979': "ФСК ЕЭС",
    '7702038150': "Московский метрополитен", #'МОСКОВСКИЙ ОРДЕНА ЛЕНИНА И ОРДЕНА ТРУДОВОГО КРАСНОГО ЗНАМЕНИ МЕТРОПОЛИТЕН ИМЕНИ В.И.ЛЕНИНА'
    '7721632827': "Концерн Росэнергоатом",
    '7706664260': "Атомэнергопром",
    '7703683145': "Холдинг ВТБ Капитал АЙ БИ"
}


def rename(df, rename_dict=SHORT_NAMES_BY_INN):
    def actor(inn):
        return rename_dict[inn]
    ix = df.loc[:, 'inn'].isin(rename_dict.keys())
    df.loc[ix, 'title'] = df.loc[ix, 'inn'].apply(actor)
    return df

import pandas as pd
x = pd.DataFrame({'title': {1134038: 'МОСКОВСКИЙ ОРДЕНА ЛЕНИНА И ОРДЕНА ТРУДОВОГО КРАСНОГО ЗНАМЕНИ МЕТРОПОЛИТЕН ИМЕНИ В.И.ЛЕНИНА'}, 
                  'inn': {1134038: '7702038150'}}
    )

assert rename(x).iloc[0,:].title == 'Московский метрополитен'


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


def canonic_df(df):
    for f in [adjust_rub, 
              add_okved_subcode, 
              add_region, 
              add_title,
              rename]:
        df = f(df)
    return df.loc[:, canonic_columns()]


def canonic_columns(numeric=SHORT_COLUMNS.numeric):
    return (['title', 'org', 'okpo', 'okopf', 'okfs', 'okved', 'inn'] +
            ['unit'] +
            ['ok1', 'ok2', 'ok3', 'region'] +
            numeric)


def get_numeric_columns(numeric=SHORT_COLUMNS.numeric):
    return numeric + ['ok1', 'ok2', 'ok3', 'region']


def canonic_dtypes():
    numerics = get_numeric_columns()

    def switch(col):
        return numpy.int64 if (col in numerics) else str
    return {col: switch(col) for col in canonic_columns()}