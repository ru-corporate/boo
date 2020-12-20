---
title: 'boo: A Python client to get financial statements for 2.5 million Russian firms (2012-2018)'
tags:
  - Python
  - economics
  - finance
  - financial statements
  - corporate reports
  - financial disclosure
authors:
  - name: Evgeniy Pogrebnyak
    orcid: 0000-0003-3914-9665
    affiliation: 1
affiliations:
 - name: Dean, Finance and Economics Department, Moscow State Institute of International Relations (Finec MGIMO)
   index: 1
date: 20 December 2020
bibliography: paper.bib
---

# Statement of Need

Financial statements of Russian firms are among the most downloaded open datasets,
released by the Russian official statistics agency (Rosstat) in 2012-2018. 
However, the raw data comes with limited metadata or column descriptions 
(who might have guessed `*_3` is current year and  `*_4` is previous year). 

Linking raw file columns to financial report entries and data cleaning are essential 
functionality of this package, while the rest are convenience features.

The 2012-2018 financial statements remain a key free open source dataset for corporate 
data as in later years similar information is released on a paid basis.

# Summary

- Why this data is useful - from a shop nearby to national champions.

- What `boo` does?

The `boo` package allows to locate and download the datasets by year, annotate columns with 
corresponding financial statements entry codes, clean data the data and present 
the dataset as `pandas` dataframe, or save it to csv of Excel file.

- Who can use `boo`? 
  - in classroom

- Example of a codebook or even a coding environment in a statistics agency.

- Limitations. 

- What are the alternatives? 
  - some dedicated 
  - paid services 

The forces on stars, galaxies, and dark matter under external gravitational
fields lead to the dynamical evolution of structures in the universe. The orbits
of these bodies are therefore key to understanding the formation, history, and
future state of galaxies. The field of "galactic dynamics," which aims to model
the gravitating components of galaxies to study their structure and evolution,
is now well-established, commonly taught, and frequently used in astronomy.
Aside from toy problems and demonstrations, the majority of problems require
efficient numerical tools, many of which require the same base code (e.g., for
performing numerical orbit integration).

``Gala`` is an Astropy-affiliated Python package for galactic dynamics. Python
enables wrapping low-level languages (e.g., C) for speed without losing
flexibility or ease-of-use in the user-interface. The API for ``Gala`` was
designed to provide a class-based and user-friendly interface to fast (C or
Cython-optimized) implementations of common operations such as gravitational
potential and force evaluation, orbit integration, dynamical transformations,
and chaos indicators for nonlinear dynamics. ``Gala`` also relies heavily on and
interfaces well with the implementations of physical units and astronomical
coordinate systems in the ``Astropy`` package [@astropy] (``astropy.units`` and
``astropy.coordinates``).

``Gala`` was designed to be used by both astronomical researchers and by
students in courses on gravitational dynamics or astronomy. It has already been
used in a number of scientific publications [@Pearson:2017] and has also been
used in graduate courses on Galactic dynamics to, e.g., provide interactive
visualizations of textbook material [@Binney:2008]. The combination of speed,
design, and support for Astropy functionality in ``Gala`` will enable exciting
scientific explorations of forthcoming data releases from the *Gaia* mission
[@gaia] by students and experts alike. The source code for ``Gala`` has been
archived to Zenodo with the linked DOI: [@zenodo]

# Acknowledgements

Daniil Chizhevskij supported the release of this package at PyPI. Without him `pip install boo` would not be possible.

[New Economic School](https://www.nes.ru) students were first to deal with this dataset 
in a classroom setting in spring 2020 "Corporate bank financing" course. Their challenging questions 
helped shape this package.

# References

- [A Realistic Guide to Making Data Available Alongside Code toImprove Reproducibility.]()
- (https://www.datafoundation.org/xbrl-report-2017)

