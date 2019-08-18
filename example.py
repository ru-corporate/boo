from boo import download, build, read_dataframe

download(2012)
build(2012)
df = read_dataframe(2012)
print(df.head())