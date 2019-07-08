from setuptools import setup, find_packages

# 0.0.2 changes folder storage to ~/.boo and exposes file location helpers 
#       raw_filepath(year) and processed_filepath(year)

# 0.0.3 migrates client to http://github.com/ru-corporate/boo 
#       and makes it minimalistic, column naming similar to csvcut,
#       filtering via pandas  

# 0.0.4 adds erase() function

setup(name='boo',
      version='0.0.4b',
      description='Russian corporate reports 2012-2017',
      url='http://github.com/ru-corporate/boo',
      author='Evgeniy Pogrebnyak',
      author_email='e.pogrebnyak@gmail.com',
      license='MIT',
      packages=find_packages(),
      zip_safe=False, 
      install_requires=[
        "requests",
        "pandas",
        "tqdm"
        ]
      )
