"""
Not necessary to use
"""

from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("data_structures.pyx"),
)
