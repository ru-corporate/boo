from boo.dataframe.canonic import is_numeric_column

B = 1_000_000

# columns


def numeric_columns(df):
    return [c for c in df.columns if is_numeric_column(c)]


def text_columns(df):
    return [c for c in df.columns if not is_numeric_column(c)]


def split_columns(df):
    return text_columns(df), numeric_columns(df), df.columns


def no_lags(df):
    return [c for c in df.columns if ("_lag" not in c)]

# rows

def is_alive(df):
    return (df.sales != 0) & (df.cf != 0) & (df.profit_before_tax != 0)

# MAYBE: large deviations

# values

def change_numeraire(df, unit):
    text_cols, num_cols, all_cols = split_columns(df)
    return df.loc[:, num_cols] \
        .divide(unit).round(1) \
        .join(df[text_cols])[all_cols]


def to_bln(df): return change_numeraire(df, unit=B)


# export

def large_companies(df):
    _df = df.loc[is_alive(df), :] \
            .query("ta > 1_000_000") \
            .sort_values("ta", ascending=False)
    return to_bln(_df)


BASE_COLUMNS = ['region', 'ok1', 'ok2', 'title'] + \
               ['ta', 'cash', 'of', 'sales', 'profit_before_tax', 'cf']
CF_COLUMNS = ['cf_oper', 'cf_inv', 'cf_fin']


def shorthand_columns(df):
    return df.rename(columns={'profit_before_tax': 'p',
                              'tp_capital': 'cap'})
                              
def less_columns(df):
    cols = no_lags(df)
    return shorthand_columns(df)[cols]

# identities:
# ta = tp
# ta_fix + ta_nonfix = ta
# tp = tp_capital + tp_long + tp_short + ...
# cf_oper + cf_inv + cf_fin = cf
