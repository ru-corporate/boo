from boo.dataframe.canonic import is_numeric_column

# columns types


def numeric_columns(df):
    return list(filter(is_numeric_column, df.columns))


def text_columns(df):
    s = set(df.columns) - set(numeric_columns(df))
    return list(s)


def split_columns(df):
    return text_columns(df), numeric_columns(df), df.columns


# change rows


def is_alive(df):
    return (df.sales != 0) | (df.cf != 0) | (df.profit_before_tax != 0)
    # MAYBE: add large deviations from accounting identity

# change values


def change_numeraire(df, unit):
    """Change unit of account (numeraire), eg thousands to billion.
       Assumes *df* units are thousand rubles.
    """
    text_cols, num_cols, all_cols = split_columns(df)
    return df.loc[:, num_cols] \
        .divide(unit).round(1) \
        .join(df[text_cols])[all_cols]


def to_bln(df):
    return change_numeraire(df, unit=1_000_000)


def to_mln(df):  # from thousands, default
    return change_numeraire(df, unit=1_000)


# export


def large_companies(df):
    _df = df.loc[is_alive(df), :] \
            .query("ta > 1_000_000") \
            .sort_values("ta", ascending=False)
    return to_bln(_df)


def medium_companies(df):
    _df = df.query("sales > 1_000") \
            .sort_values("sales", ascending=False)
    return to_mln(_df)


def shorthand(df):
    return df.rename(columns={'profit_before_tax': 'p',
                              'profit_before_tax_lag': 'p_lag',
                              'tp_capital': 'cap',
                              'tp_capital_lag': 'cap_lag'})


def no_lags(df):
    return df[[c for c in df.columns if ("_lag" not in c)]]


class Columns:
    MINIMAL = ['region', 'ok1', 'ok2', 'title'] + \
              ['ta', 'of', 'sales', 'profit_before_tax', 'cf']
    CF = ['cf_oper', 'cf_inv', 'cf_fin']


def minimal_columns(df):
    return shorthand(df[Columns.MINIMAL])

# Identities:
#   ta = tp
#   ta_fix + ta_nonfix = ta
#   tp = tp_capital + tp_long + tp_short + ...
#   cf_oper + cf_inv + cf_fin = cf
