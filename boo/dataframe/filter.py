from boo.dataframe.canonic import is_numeric_column

B = 1_000_000

# columns types

def numeric_columns(df):
    return list(filter(is_numeric_column, df.columns))


def text_columns(df):
    s = set(df.columns) - set(numeric_columns(df))
    return list(s)


def split_columns(df):
    return text_columns(df), numeric_columns(df), df.columns

# rows

def is_alive(df):
    return (df.sales != 0) & (df.cf != 0) & (df.profit_before_tax != 0)
    # MAYBE ADD: large deviations from accounting identity

# values

def change_numeraire(df, unit):
    """Change unit of account (numeraire), eg thousands to billion."""
    text_cols, num_cols, all_cols = split_columns(df)
    return df.loc[:, num_cols] \
        .divide(unit).round(1) \
        .join(df[text_cols])[all_cols]


def to_bln(df): 
    return change_numeraire(df, unit=B)
    

# export

def large_companies(df):
    _df = df.loc[is_alive(df), :] \
            .query("ta > 1_000_000") \
            .sort_values("ta", ascending=False)
    return to_bln(_df)

def shorthand(df):
    return df.rename(columns={'profit_before_tax': 'p',
                              'profit_before_tax_lag': 'p_lag',
                              'tp_capital': 'cap',
                              'tp_capital_lag': 'cap_lag'},
                     errors='ignore')
                              
def less_columns(df):
    cols = no_lags(df)
    return shorthand(df[cols])

class ColumnSubset:
    MINIMAL = ['region', 'ok1', 'ok2', 'title'] + \
              ['ta', 'of', 'sales', 'profit_before_tax', 'cf']
    CF = ['cf_oper', 'cf_inv', 'cf_fin']

def minimal_columns(df):
    return shorthand(df[ColumnSubset.MINIMAL]) 

# identities:
# ta = tp
# ta_fix + ta_nonfix = ta
# tp = tp_capital + tp_long + tp_short + ...
# cf_oper + cf_inv + cf_fin = cf
