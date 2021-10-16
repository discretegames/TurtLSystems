"""Package setup file for the Python 3 TurtLSystems package: https://pypi.org/project/TurtLSystems"""

from setuptools import setup, find_packages

version = "0.0.1"

setup(name='TurtLSystems', version=version, author='discretegames',
      url='https://github.com/discretegames/TurtLSystems',
      packages=find_packages('src'),
      package_dir={'': 'src'})
