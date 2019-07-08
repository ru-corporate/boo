[![colab](https://img.shields.io/badge/colab-launch-blue.svg)](https://colab.research.google.com/drive/1BGLalP4rr5FdtXsEzb5oG4sHL5qmgbAS#scrollTo=YuW47K8E4IBZ)

# boo
Python client for Rosstat corporate reports


#### Goal

Access balance sheet, profit and loss and cash flow statements of Russian firms.


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
