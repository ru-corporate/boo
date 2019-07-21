"""boo-work.ipynb

Original file is located at
    https://colab.research.google.com/drive/1uNvXUuC-HqtsSguQVAQ-X9C-_r4k91M-

For install:
    pip install --upgrade boo

For development version use:
    pip install --upgrade git+https://github.com/ru-corporate/boo.git@master
"""

from  boo.preset import large_companies, sort, industry, contains

#raw_df = boo.read_dataframe(2017)
print ("Read dataframe, processing..." )
df_large = preset_large_companies(raw_df)
print("Done")

print("Действующие крупные компании")
print("Количество компаний (исходное):      ", raw_df.shape[0])
print("Количество компаний (после фильтров):", df_large.shape[0])

sort(df_large, 'ta').head(100)

sort(df_large, "p").head(50)

"""# Регионы"""

sort(region(df_large, 2),"ta")

"""### Смотрим отдельные холдинги"""

 # Мы видим только российские активы https://www.interrao.ru/company/structure/
sort(contains(df_large, "ИНТЕР РАО"), "ta").head(10)

sort(contains(df_large, "ЛУКОЙЛ"), "ta").head(10)

# Газпром нефть - отдельное юрлицо "5504036333"
x = sort(contains(df_large, "Газпром"), "ta")
x[x.index != "5504036333"].head(10)

"""### Смотрим отрасли"""

sort(industry(df_large, 64), "ta").head(10)


dfta = sort(df_large, "ta")
for i in boo.okved_codes_v2():
   x = industry(dfta, i).head(20)
   if not x.empty:
      print (i, boo.okved_name_v2(i))
      print (x.to_string(line_width=200))


