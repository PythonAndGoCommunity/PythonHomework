"""
This module allows to installs the application
"""
from setuptools import setup, find_packages

setup(
    name='pycalc',
    version='1.0',
    packages=find_packages(),
    py_modules=['main'],
    entry_points={
        'console_scripts': ['pycalc = pycalc.main:main']
    }
)
