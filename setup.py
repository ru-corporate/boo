from setuptools import setup, find_packages
from pathlib import Path

# 0.0.2 changes folder storage to ~/.boo and exposes file location helpers 
#       raw_filepath(year) and processed_filepath(year)

# 0.0.3 migrates client to http://github.com/ru-corporate/boo 
#       and makes it minimalistic, column naming is similar to csvcut,
#       filtering done via pandas  

# 0.0.4 adds wipe() and wipe_all() functions

# 0.0.5 README will surface on PyPi

#0.0.6 additional dataset cleaning moved from notebook to package

#0.0.7 help messages and whatis() function

setup(name='boo',
      version='0.0.7',
      description='Russian corporate reports 2012-2017',
      url='http://github.com/ru-corporate/boo',
      author='Evgeniy Pogrebnyak',
      author_email='e.pogrebnyak@gmail.com',
      license='MIT',
      packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
      long_description = Path("README.md").read_text(),
      long_description_content_type="text/markdown",
      zip_safe=False, 
      install_requires=[
        "requests",
        "pandas",
        "tqdm"
        ],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Financial and Insurance Industry",  
        "Topic :: Office/Business :: Financial",    
        "Topic :: Utilities"
      ]
      )
