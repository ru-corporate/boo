import pandas as pd
from matplotlib import pyplot as plt

import boo


def ebitda_proxy(df):
    """Оценка EBITDA.
    
       В отчетности нет амортизации, используем близкие по смыслу показатели 
       из cash flow. EBITDA считается на показателях отчета о прибылях и убытках.
       
    """
    return df.cf_oper_in - df.paid_to_supplier - df.paid_to_worker


def add_ratios(df):
    df["profit_to_sales"] = df.profit_before_tax / df.sales
    df["sales_to_assets"] = df.sales / df.ta
    df["ir"] = df.exp_interest / (df.debt_long + df.debt_short)
    df["na"] = df.ta - df.tp_long - df.tp_short
    df["ebitda_e"] = ebitda_proxy(df)
    # HW: add more finanical ratios
    return df


def unlag(df):
    return [col for col in df.columns if not col.endswith("lag")]


def sort(df, col):
    return df.sort_values(col, ascending=False)


# df = pd.read_csv("processed_2018.csv").set_index('inn')
url = "https://boodata.s3.eu-central-1.amazonaws.com/processed_2018.csv"
df = pd.read_csv(url).set_index("inn")
df = add_ratios(df)
all_columns = unlag(df)
cols = "ok1 title ta sales".split()
df[cols]
assert boo.whatis("of") == "Основные средства"


# Check accounting identities
checks = dict(
    balance=df.ta - df.tp,
    assets=df.ta_fix + df.ta_nonfix - df.ta,
    liab=df.tp_capital + df.tp_long + df.tp_short - df.tp,
    cash_flow=df.cf_oper + df.cf_inv + df.cf_fin - df.cf,
    delta_cash=df.cash - df.cash_lag - df.cf,
)

for name in checks.keys():
    plt.figure()
    checks[name].hist(log=True)
    plt.title(name)


# Create 'other' variables
df["ta_fix_other"] = df.ta_fix - df.of
df["ta_nonfix_other"] = df.ta_nonfix - df.cash
df["tp_short_other"] = df.tp_short - df.debt_short - df.payables  # overwriting
df["tp_long_other"] = df.tp_long - df.debt_long


# Пример АвтоВАЗа - наши данные и данные из Интернета совпадают

# https://www.list-org.com/company/36
# ИНН 6320002223
# БАЛАНС (актив)	151423000

# HW: add data for different company

expected = dict(inn=6320002223, values=dict(ta=151423000))
inn = expected["inn"]
for var, x in expected["values"].items():
    assert df.loc[inn, var] == round(x / 1_000_000, 1)

# Проценты
plt.scatter(x=df.exp_interest, y=df.paid_interest, alpha=0.5)
plt.xlabel("Начисленные проценты")
plt.ylabel("Выплаченные проценты")
lim = 60
plt.xlim(0, lim)
plt.ylim(0, lim)

# Фондоотдача
plt.figure()
min_ta = 100
v = sort(df, "sales_to_assets").query(f"ta>{min_ta}")
plt.scatter(x=v.ta.cumsum(), y=v.sales_to_assets, s=0.5)
plt.xlabel("Активы (накопленным итогом)")
plt.ylabel("Выручка / активы")
v.head(20)[cols]


def fit_screen(df, cols=cols):
    df = df.copy()
    df["title"] = df.title.apply(lambda x: x[:30])
    cols_ = cols + ["profit_before_tax"]
    return df[cols_].rename(columns={"profit_before_tax": "p"})


# Рентабельность
plt.figure()
min_ta = 100
what = "profit_to_sales"
s = sort(df, what).query(f"ta>{min_ta}")
s = s[20:-20]
plt.scatter(x=s.ta.cumsum(), y=s[what], s=0.5)
plt.xlabel("Активы (накопленным итогом)")
plt.ylabel(what)
s = fit_screen(s)
s.head(20)

"""
Задание:
    
1. Выберите одну компанию и проверьте несколько цифр ее отчетности    
   по данным web-сайта компании (по примеру АвтоВАЗа) или 
   агрегатора статистики типа https://www.list-org.com/
   
   Желательно взять цифры из разных разделов отчетности. 
   
   Обратите внимание, что данные могут быть переведены в 
   млн. или млрд. рублей и округлены. 
   

2. Добавьте финансовые показатели в функцию add_ratios(). Этих показателей
   может быть довольно много, приветствутеся, если вы сгруппируете   
   их (например, ликвидность, рентабельность, финансовая устойчивость).
   
   В комментарии в коде кратко объясните логику показателя или дайте ему 
   характерное название. Можете указать показатели, которые вы бы хотели,
   посчитать на основе бухгалтерской отчетности, но у вас не хватает данных.
   
   Опционально: попробуйте построить распределение этого предложенных 
                показателей для на сформированной в этом примере выборке.

   Справочно: вид форм, которые раскрыывают компании по РСБУ определяется    
   Приложение N 4 к приказу Минфина РФ от 2 июля 2010 г. N 66н
   http://ivo.garant.ru/#/document/12177762/paragraph/110832:0


3. Дополнительно / обсуждение:

   - заполнить несколько позиций в `my_inn`
   - предложения по другим проверкам или показателям (free cash flow?)
   - идеи как улучшить показатель ebitda_proxy()
   - показатели cash-flow холдинговых компаний
   - какое поведение компаний мы молги бы показать на этой отчетности
     (например, инвестицонная фаза проекта)
   - какие показатели нужно ввести, чтобы уточнить расчет "прочих" переменных  
   - предложения по визуализациям использованным в презентации   
"""


"""
Далее:
  - компании-банкроты
  - инвестиции
  - свертка показателей Altman Z-score
  - проверть балансовые равенства на исходных данных source_df   
  - график показателей "все-против-всех"
"""
