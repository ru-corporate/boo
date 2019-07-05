"""Преобразовать данные: 

- Ввести новые названия столбцов, отражающие смысл переменных отчетности
- Уменьшить размер файла за счет удаления столбцов с числовыми данными, 
    не указанными в *columns_dict*
- Привести все строки к одинаковым единицам измерения (тыс. руб.)
- Новые колонки: 
    * найти короткое название компании
    * код ОКВЭД разбить на три уровня
    * определить регион по ИНН

"""
from collections import OrderedDict
from numpy import int64

INT_TYPE = int64
EMPTY = int('0')
QUOTE_CHAR = '"'


# transform numbers
def rub_to_thousand(x: int):
    return int(round(0.001 * float(x)))


def mln_to_thousand(x: int):
    return 1000 * int(x)


def identity(x):
    return int(x)


# transform strings
def okved3(code_string: str):
    """Get 3 levels of OKVED codes from *code_string*."""
    codes = [int(x) for x in code_string.split(".")]
    return codes + [EMPTY] * (3 - len(codes))


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


def get_unit_adjuster(unit_name: str):
    mapper = {'383': rub_to_thousand,
              '385': mln_to_thousand,
              '384': identity}
    try:
        return mapper[unit_name]
    except KeyError:
        raise ValueError("Unit not supported: %s" % unit_name)


def make_text_values(rowd: OrderedDict):
    # assemble new text columns
    ok1, ok2, ok3 = okved3(rowd['okved'])
    org, title = dequote(rowd['name'])
    region = rowd['inn'][0:2]
    return [ok1, ok2, ok3,
            org, title, region, rowd['inn'],
            rowd['okpo'], rowd['okopf'], rowd['okfs']]


def make_text_keys():
    return ['ok1', 'ok2', 'ok3',
            'org', 'title', 'region', 'inn',
            'okpo', 'okopf', 'okfs']

def new_text_field_name(varname: str):
    okv = lambda text: f"Код ОКВЭД {text} уровня"
    return {'ok1': okv("первого"), 
            'ok2': okv("второго"),
            'ok3': okv("третьего"),
            'org': "Тип юридического лица (часть наименования организации)",
            'title': "Короткое название организации",
            'region': "Код региона по ИНН"}.get(varname)                            


def make_data_values(rowd: OrderedDict, data_columns):
    # adjust values to '000 rub
    func = get_unit_adjuster(unit_name=rowd['unit'])
    return [func(rowd[k]) for k in data_columns]


def values_getter(data_columns):
    return lambda rowd: make_text_values(rowd) + make_data_values(rowd, data_columns)


def to_dict_maker(all_columns):
    return lambda row: OrderedDict(zip(all_columns, row))


def colnames(data_columns):
    return make_text_keys() + data_columns


def dtypes(colnames):
    """Return types correspoding to column.long_colnames().
       Used to speed up CSV import.
    """
    dtype_dict = {k: INT_TYPE for k in colnames}
    for key in ['org', 'title', 'region', 'inn',
                'okpo', 'okopf', 'okfs',
                'unit', 'date_published']:
        if key in colnames:
            dtype_dict[key] = str
    return dtype_dict


class Reader:
    def __init__(self, all_columns, data_columns, **kwarg):
        self.to_dict = to_dict_maker(all_columns)
        self.parse_ordered_dict = values_getter(data_columns)
        self.colnames = colnames(data_columns)
        self.dtypes = dtypes(self.colnames)
        
    def parse_row(self, items):
        return self.parse_ordered_dict(self.to_dict(items))      
    