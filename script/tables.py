from tabulate import tabulate

from boo import file_length_mb

# File lengths
h = [(year, file_length_mb(year)) for year in range(2012, 2017 + 1)]
print(tabulate(h, headers=["Year", "Size (Mb)"], tablefmt="github"))
print()
