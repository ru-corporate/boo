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

# """## Другие интересные задачи

""" 1. Постройте корреляционную материцу между показателями отчетености. Какие из пар показателей вы можете прокомментировать?
# 2. Как компании платят по долгам? Сравните `exp_interest` и `paid_interest`. Видите ли вы компании - банкроты?
# 3. Какие компании инвестируют в основые средства? Сравните прирост основных средств и величину расходов на капвложения `paid_fa_investment`.
# 4. Найдите компании - холдинги (обычно нет операционной выручки,  есть долгосрочные активы, денежный поток от финансовой или инвестицонной деятельности)
# 5. Постройте аналог кредитного рейтинга компаний по [модели Альтмана](https://ru.wikipedia.org/wiki/%D0%9C%D0%BE%D0%B4%D0%B5%D0%BB%D1%8C_%D0%90%D0%BB%D1%8C%D1%82%D0%BC%D0%B0%D0%BD%D0%B0). Как бы вы подошли к определению коэффициентов модели?
# 6. Какое название компании самое часто распространенное в России?
# 7. Cравните результаты предыдущего раздела по выборкам крупных компаний с рейтингами Эксперт, PБК, Forbes, Коммерсант.

# Задания можно делать сначала для всей выборки, затем для подвыборки компаний, чтобы получить более интерпретируемые результаты.
# """