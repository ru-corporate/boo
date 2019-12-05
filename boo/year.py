from boo.errors import WrongYearError

# Must manually hardcode new timestamps when new version arrives
TIMESTAMPS = {2012: 20190329,
              2013: 20190411,
              2014: 20190411,
              2015: 20190411,
              2016: 20190411,
              2017: 20190423,
              2018: 20191029, # from data-20191029t000000-structure-20181231t000000.csv              
              }

YEARS = list(TIMESTAMPS.keys())

def make_url(year: int) -> str:
    """
    Construct URL similar to
    http://www.gks.ru/opendata/storage/7708234640-bdboo2012/data-20181029t000000-structure-20121231t000000.csv
    """
    if year in [0, 1]:
        pat ='https://raw.githubusercontent.com/ru-corporate/boo/master/assets/sample{}.txt'
        return pat.format(year)
    try:
        timestamp = TIMESTAMPS[year]
        return ('http://www.gks.ru/opendata/storage/'
                f'7708234640-bdboo{year}/'
                f'data-{timestamp}t000000-structure-'
                f'{year}1231t000000.csv'
                )
    except KeyError:
        raise WrongYearError(year)
