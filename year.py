YEAR_0 = 2012
YEAR_LAST = 2017
TIMESTAMPS = {2012:20190329, 2017:20190423}


def is_valid(year):
    return (YEAR_0 <= year <= YEAR_LAST) or year == 0


def validate(year):
    if is_valid(year):
        print("Year:", year)    
    else:    
        raise ValueError(f"Year not supported: {year}. Must be {YEAR_0}-{YEAR_LAST}")


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
    
