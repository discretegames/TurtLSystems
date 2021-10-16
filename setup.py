"""Package setup file for TurtLSystems Python 3 package (https://pypi.org/project/TurtLSystems)."""

from setuptools import setup, find_packages

VERSION = "0.0.2"

setup(name='TurtLSystems', version=VERSION, author='discretegames',
      url='https://github.com/discretegames/TurtLSystems',
      packages=find_packages('src'),
      package_dir={'': 'src'})
