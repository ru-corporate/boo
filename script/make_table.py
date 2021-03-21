import pandas as pd


def mb(x):
    return int(round(x / (2 ** 10) ** 2, 0))


df = pd.DataFrame(
    [
        (year, mb(file_length(year)), mb(size(path_csv(year))))
        for year in available_years()
    ],
    columns=["Year", "ZIP (Mb)", "CSV (Mb)"],
).set_index("Year")
df = df.applymap(str)
print(df.to_markdown())
