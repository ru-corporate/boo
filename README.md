# boo
Python client for Rosstat corporate reports

Install:

```
pip install git+https://github.com/ru-corporate/boo.git@master
```

Usage:

```python
from boo import acquire

df = acquire(2012)
print(df.head())

```
