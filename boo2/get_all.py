from boo import available_years, download, unpack  # read_intermediate_df

dfs = dict()
for year in available_years():
    download(year)
    unpack(year)
    dfs[year] = read_intermediate_df(year, nrows=100)


"""
pip install boo
mkdir boo_data
boo download 2012 --dir boo_data
boo unpack 2012 --dir boo_data
boo data 2012 --nrows 5 --dir boo_data
boo path 2012 --csv --dir boo_data
boo wipe 2012 --csv --dir boo_data
"""
