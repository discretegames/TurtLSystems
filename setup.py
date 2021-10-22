"""Package setup file for turtlsystems Python package (https://pypi.org/project/turtlsystems)."""

from pathlib import Path
from setuptools import setup, find_packages

VERSION = "0.0.5"

with open(Path(__file__).with_name('README.md'), encoding='utf-8') as file:
    long_description = file.read()

setup(name='turtlsystems', version=VERSION, author='discretegames',
      url='https://github.com/discretegames/turtlsystems',
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=find_packages('src'),
      package_dir={'': 'src'})
