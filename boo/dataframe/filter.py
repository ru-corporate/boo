from boo.dataframe.canonic import is_numeric_column

B = 1_000_000
TEXT_COLUMNS = ['region', 'ok1', 'ok2', 'title']
NUMERIC_COLUMNS = ['ta', 'cash', 'of', 'sales', 'profit_before_tax', 'cf']
CHANGE_NAMES = {'profit_before_tax': 'p'}

def numeric_columns(df):
    return [c for c in df.columns if is_numeric_column(c)]


def is_alive(df):
    return (df.sales != 0) & (df.cf != 0) & (df.profit_before_tax != 0)


def large_companies(df, 
                    text_columns=TEXT_COLUMNS, 
                    numeric_columns=NUMERIC_COLUMNS,
                    rename_dict=CHANGE_NAMES):
    return df.loc[is_alive(df), numeric_columns] \
        .query("ta > 1_000_000") \
        .divide(B).round(1) \
        .sort_values("ta", ascending=False) \
        .join(df[text_columns])[text_columns+numeric_columns] \
        .rename(columns=rename_dict)