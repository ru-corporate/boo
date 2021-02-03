from get_file import available_years, download, read_intermediate_df

for year in available_years():
    download(year)
    read_intermediate_df(year, nrows=100)
