TIMESTAMPS = {2012:20190329, 
              2013:20190331,
              2014:20190411,
              2015:20190411,
              2016:20190411,
              2017:20190423}

YEARS = list(TIMESTAMPS.keys())

def is_valid(year):
    return (year in YEARS) or year == 0


def validate(year):
    if is_valid(year):
        print("Year:", year)    
    else:    
        raise ValueError(f"Year not supported: {year}. Must be one of {YEARS}")


def make_url(year):
    """
    Construct URL similar to
    http://www.gks.ru/opendata/storage/7708234640-bdboo2012/data-20181029t000000-structure-20121231t000000.csv
    """
    timestamp = TIMESTAMPS.get(year)
    if year == 0:
        return 'https://raw.githubusercontent.com/ru-corporate/sandbox/master/assets/sample.txt'
    return ('http://www.gks.ru/opendata/storage/' +
            f'7708234640-bdboo{year}/' +
            f'data-{timestamp}t000000-structure-{year}1231t000000.csv'
            )
    
