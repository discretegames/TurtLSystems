"""Package setup file for TurtLSystems Python 3 package (https://pypi.org/project/TurtLSystems)."""

from setuptools import setup, find_packages
from pathlib import Path

VERSION = "0.0.3"

with open(Path(__file__).with_name('README.md'), encoding='utf-8') as file:
    long_description = file.read()

setup(name='TurtLSystems', version=VERSION, author='discretegames',
      url='https://github.com/discretegames/TurtLSystems',
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=find_packages('src'),
      package_dir={'': 'src'})
