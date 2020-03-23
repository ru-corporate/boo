"""Преобразование сырых названий столбцов в названия переменных.

1) Список названий переменных
   TTL_COLUMNS: [str] -> MAPPER: dict -> SHORT_COLUMNS: Columns

2) Функция для получения укороченного ряда данных  
   TTL_COLUMNS: [str] -> MAPPER: dict -> CONVERTER_FUNC: [str] -> [str]

3) Поиск кода поназванию переменных
   MAPPER: dict -> name_to_code: (str -> str)

# Описания полей отчетности можно посмотреть например в:
# http://info.avtovaz.ru/files/avtovaz_ras_fs_2012_rus_secured.pdf

# Более подробно о формах:
# http://www.consultant.ru/document/cons_doc_LAW_103394/b990bf4a13bd23fda86e0bba50c462a174c0d123/#dst100515
"""

from collections import OrderedDict
from typing import List, Tuple
from dataclasses import dataclass

import numpy

# Column names as provided at Rosstat web site
TTL_COLUMNS = [
    "Наименование",
    "ОКПО",
    "ОКОПФ",
    "ОКФС",
    "ОКВЭД",
    "ИНН",
    "Код единицы измерения",
    "Тип отчета",
    "11103",
    "11104",
    "11203",
    "11204",
    "11303",
    "11304",
    "11403",
    "11404",
    "11503",
    "11504",
    "11603",
    "11604",
    "11703",
    "11704",
    "11803",
    "11804",
    "11903",
    "11904",
    "11003",
    "11004",
    "12103",
    "12104",
    "12203",
    "12204",
    "12303",
    "12304",
    "12403",
    "12404",
    "12503",
    "12504",
    "12603",
    "12604",
    "12003",
    "12004",
    "16003",
    "16004",
    "13103",
    "13104",
    "13203",
    "13204",
    "13403",
    "13404",
    "13503",
    "13504",
    "13603",
    "13604",
    "13703",
    "13704",
    "13003",
    "13004",
    "14103",
    "14104",
    "14203",
    "14204",
    "14303",
    "14304",
    "14503",
    "14504",
    "14003",
    "14004",
    "15103",
    "15104",
    "15203",
    "15204",
    "15303",
    "15304",
    "15403",
    "15404",
    "15503",
    "15504",
    "15003",
    "15004",
    "17003",
    "17004",
    "21103",
    "21104",
    "21203",
    "21204",
    "21003",
    "21004",
    "22103",
    "22104",
    "22203",
    "22204",
    "22003",
    "22004",
    "23103",
    "23104",
    "23203",
    "23204",
    "23303",
    "23304",
    "23403",
    "23404",
    "23503",
    "23504",
    "23003",
    "23004",
    "24103",
    "24104",
    "24213",
    "24214",
    "24303",
    "24304",
    "24503",
    "24504",
    "24603",
    "24604",
    "24003",
    "24004",
    "25103",
    "25104",
    "25203",
    "25204",
    "25003",
    "25004",
    "32003",
    "32004",
    "32005",
    "32006",
    "32007",
    "32008",
    "33103",
    "33104",
    "33105",
    "33106",
    "33107",
    "33108",
    "33117",
    "33118",
    "33125",
    "33127",
    "33128",
    "33135",
    "33137",
    "33138",
    "33143",
    "33144",
    "33145",
    "33148",
    "33153",
    "33154",
    "33155",
    "33157",
    "33163",
    "33164",
    "33165",
    "33166",
    "33167",
    "33168",
    "33203",
    "33204",
    "33205",
    "33206",
    "33207",
    "33208",
    "33217",
    "33218",
    "33225",
    "33227",
    "33228",
    "33235",
    "33237",
    "33238",
    "33243",
    "33244",
    "33245",
    "33247",
    "33248",
    "33253",
    "33254",
    "33255",
    "33257",
    "33258",
    "33263",
    "33264",
    "33265",
    "33266",
    "33267",
    "33268",
    "33277",
    "33278",
    "33305",
    "33306",
    "33307",
    "33406",
    "33407",
    "33003",
    "33004",
    "33005",
    "33006",
    "33007",
    "33008",
    "36003",
    "36004",
    "41103",
    "41113",
    "41123",
    "41133",
    "41193",
    "41203",
    "41213",
    "41223",
    "41233",
    "41243",
    "41293",
    "41003",
    "42103",
    "42113",
    "42123",
    "42133",
    "42143",
    "42193",
    "42203",
    "42213",
    "42223",
    "42233",
    "42243",
    "42293",
    "42003",
    "43103",
    "43113",
    "43123",
    "43133",
    "43143",
    "43193",
    "43203",
    "43213",
    "43223",
    "43233",
    "43293",
    "43003",
    "44003",
    "44903",
    "61003",
    "62103",
    "62153",
    "62203",
    "62303",
    "62403",
    "62503",
    "62003",
    "63103",
    "63113",
    "63123",
    "63133",
    "63203",
    "63213",
    "63223",
    "63233",
    "63243",
    "63253",
    "63263",
    "63303",
    "63503",
    "63003",
    "64003",
    "Дата актуализации",
]

# -- Текстовые поля
TEXT_FIELDS = OrderedDict(
    [
        ("Наименование", "name"),
        ("ОКПО", "okpo"),
        ("ОКОПФ", "okopf"),
        ("ОКФС", "okfs"),
        ("ОКВЭД", "okved"),
        ("ИНН", "inn"),
        ("Код единицы измерения", "unit"),
        ("Тип отчета", "report_type"),
        ("Дата актуализации", "date_published"),
    ]
)

# --  Баланс
balance = [
    ("1100", "ta_fix"),
    ("1150", "of"),
    ("1200", "ta_nonfix"),
    ("1250", "cash"),
    ("1600", "ta"),
    ("1300", "tp_capital"),
    ("1400", "tp_long"),
    ("1410", "debt_long"),
    ("1500", "tp_short"),
    ("1510", "debt_short"),
    ("1520", "payables"),
    ("1530", "tp_short_future_income"),
    ("1540", "tp_short_estimated"),
    ("1550", "tp_short_other"),
    ("1700", "tp"),
]

# --  ОПУ
opu = [
    ("2110", "sales"),
    ("2200", "profit_oper"),
    ("2330", "exp_interest"),
    ("2300", "profit_before_tax"),
    ("2400", "profit_after_tax"),
]

# --  ОДДС
cf_total = [("4400", "cf")]

cf_oper = [
    # -- Операционная деятельность
    ("4100", "cf_oper"),
    ("4110", "cf_oper_in"),
    ("4111", "cf_oper_in_sales"),
    ("4120", "cf_oper_out"),
    ("4121", "paid_to_supplier"),
    ("4122", "paid_to_worker"),
    ("4123", "paid_interest"),
    ("4124", "paid_profit_tax"),
    ("4129", "paid_other_costs"),
]

cf_inv = [
    # -- Инвестицонная деятельность
    ("4200", "cf_inv"),
    ("4210", "cf_inv_in"),
    ("4220", "cf_inv_out"),
    ("4221", "paid_fa_investment"),
]

cf_fin = [
    # -- Финансовая деятельность
    ("4300", "cf_fin"),
    ("4310", "cf_fin_in"),
    ("4320", "cf_fin_out"),
]

DATA_FIELDS = OrderedDict(balance + opu + cf_total + cf_oper + cf_inv + cf_fin)
MAPPER = {**TEXT_FIELDS, **DATA_FIELDS}


def code_to_varname(code: str, mapper: dict = MAPPER):
    return mapper.get(code, code)


def reverse(mapper):
    return {name: code for code, name in mapper.items()}


def varname_to_code(varname: str, mapper=MAPPER):
    return reverse(mapper).get(varname, None)


def split(text: str) -> Tuple[str, bool]:
    def fst(text):
        return text[0]

    def last(text):
        return text[-1]

    def trim(text):
        return text[0:-1]

    code = text
    is_lagged = False
    if fst(text) != "3" and last(text) in ["3", "4"]:
        code = trim(text)
        if last(text) == "4":
            is_lagged = True
    return code, is_lagged


@dataclass
class Columns:
    all: [str]
    numeric: [str]

    @property
    def text(self):
        return [item for item in self.all if item not in self.numeric]

    def _switch(self, item):
        return numpy.int64 if (item in self.numeric) else str

    @property
    def dtypes(self):
        return {c: self._switch(c) for c in self.all}


@dataclass
class ColumnLabel:
    code: str
    lagged: bool

    def __str__(self):
        return self.code + ("_lag" if self.lagged else "")


Labels = List[ColumnLabel]


def rename_with(x: ColumnLabel, mapper: dict) -> ColumnLabel:
    return ColumnLabel(code=code_to_varname(x.code, mapper), lagged=x.lagged)


def as_labels(columns: [str]) -> Labels:
    return [ColumnLabel(*split(x)) for x in columns]


def update_with(colnames: Labels, mapper: dict) -> Labels:
    return [rename_with(x, mapper) for x in colnames]


def get_index(columns: [str], mapper: dict):
    xs = as_labels(columns)
    ys = update_with(xs, mapper)
    n = len(xs)
    return [i for (x, y, i) in zip(xs, ys, range(n)) if x != y]


def columns_picked_and_renamed(columns=TTL_COLUMNS, mapper=MAPPER):
    xs = as_labels(columns)
    ys = update_with(xs, mapper)
    return [str(y) for (x, y) in zip(xs, ys) if x != y]


def unlag(s: str) -> str:
    return s[:-4] if s.endswith("_lag") else s


def filter_by(columns: [str], mapper: dict) -> [str]:
    return [s for s in columns if unlag(s) in mapper.values()]


# Renamed columns
short_all = columns_picked_and_renamed(columns=TTL_COLUMNS, mapper=MAPPER)
short_num = filter_by(columns=short_all, mapper=DATA_FIELDS)
SHORT_COLUMNS = Columns(all=short_all, numeric=short_num)
SHORT_INDEX = get_index(columns=TTL_COLUMNS, mapper=MAPPER)
