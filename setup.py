from setuptools import setup, find_packages
from pathlib import Path

from changelog import version_str

# Use script upload.bat to update pipy package.

with open("README.md", encoding="utf-8") as file:
    readme_str = "\n".join(file.readlines())

setup(
    name="boo",
    version=version_str,
    description="Russian corporate reports 2012-2018",
    url="http://github.com/ru-corporate/boo",
    author="Evgeniy Pogrebnyak",
    author_email="e.pogrebnyak@gmail.com",
    license="MIT",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    long_description=readme_str,
    long_description_content_type="text/markdown",
    zip_safe=False,
    install_requires=["requests", "pandas", "tqdm"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial",
        "Topic :: Utilities",
    ],
)
