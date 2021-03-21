from boo import available_years, download, read_intermediate_df, unpack

dfs = dict()
for year in [0] + available_years():
    download(year)
    unpack(year)
    dfs[year] = read_intermediate_df(year, nrows=100)
    print(dfs[year].head(3))
