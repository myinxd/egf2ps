#!/usr/bin/env/ python3
#
# Copyright (c) 2016 Zhixian MA <zxma_sjtu@qq.com>
# MIT license
#
# References:
# [1] Python Packaging User Guide
#     https://packaging.python.org/

import os
import sys

from setuptools import setup, find_packages
# from setuptools.command.test import test as TestCommand

import egf2ps as pkg

def read(filename):
    return open(os.path.join(os.path.dirname(__file__),filename)).read()

# Check python version
if sys.version_info < (3,4):
    sys.exit("Python >= 3.4 is required...")

setup(
    name=pkg.__pkgname__,
    version=pkg.__version__,
    description=pkg.__description__,
    long_description=read("README.md"),
    author=pkg.__author__,
    author_email=pkg.__author_email__,
    url=pkg.__url__,
    license=pkg.__license__,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Scientific/Engineering :: Signal processing",
    ],
    packages=find_packages(exclude=["docs","tests"]),
    scripts=[
        "bin/egf2ps",
    ],
    install_requires=[
        "numpy",
        "scipy",
        "pandas",
        "matplotlib",
        "astropy",
        "pyregion",
        "configobj",
    ],
)
