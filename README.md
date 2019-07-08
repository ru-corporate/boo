# boo
Python client for Rosstat corporate reports

#### Install

```
pip install git+https://github.com/ru-corporate/boo.git@master
```

#### Usage

```python
from boo import prepare, read_dataframe

prepare(2012)
df = read_dataframe(2012)
print(df.head())
```
