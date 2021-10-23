"""Package setup file for TurtLSystems Python package (https://pypi.org/project/TurtLSystems)."""

from pathlib import Path
from setuptools import setup, find_packages

VERSION = "0.0.12"

if __name__ == '__main__':
    with open(Path(__file__).with_name('README.md'), encoding='utf-8') as file:
        long_description = file.read()

    setup(name='TurtLSystems',
          version=VERSION,
          author='discretegames',
          author_email='discretizedgames@gmail.com',
          url='https://github.com/discretegames/TurtLSystems',
          description="A tool to draw L-systems with turtle graphics and output them as pngs and gifs.",
          long_description=long_description,
          long_description_content_type="text/markdown",
          packages=find_packages('src'),
          package_dir={'': 'src'},
          license='MIT',
          keywords=['lsystem', 'Lindenmayer', 'system', 'fractal', 'pattern',
                    'art', 'animation', 'png', 'gif', 'turtle', 'graphics', 'designs', 'tree',
                    'Sierpinski triangle', 'Koch curve', 'dragon curve', 'Cantor', 'Barnsley fern'],
          project_urls={"GitHub": "https://github.com/discretegames/TurtLSystems",
                        "PyPI": "https://pypi.org/project/TurtLSystems",
                        "TestPyPI": "https://test.pypi.org/project/TurtLSystems"},
          python_requires='>=3.6',
          install_requires=[
              'Pillow>=6.2.0',
          ],
          classifiers=[
              "Development Status :: 3 - Alpha",
              "Intended Audience :: Education",
              "Intended Audience :: Science/Research",
              "License :: OSI Approved :: MIT License",
              "Topic :: Artistic Software",
              "Topic :: Education",
              "Topic :: Multimedia :: Graphics",
              "Topic :: Multimedia :: Graphics :: Editors :: Vector-Based",
              "Topic :: Scientific/Engineering :: Mathematics",
              "Topic :: Scientific/Engineering :: Visualization",
              "Typing :: Typed",
              "Programming Language :: Python :: 3",
              "Programming Language :: Python :: 3.6",
              "Programming Language :: Python :: 3.7",
              "Programming Language :: Python :: 3.8",
              "Programming Language :: Python :: 3.9",
              "Programming Language :: Python :: 3.10"
          ])
