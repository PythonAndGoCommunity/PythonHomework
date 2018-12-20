"""
This module allows to installs the application
"""
import setuptools 

setuptools.setup(
    name='pycalc',
    version='1.0',
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': ['pycalc = pycalc.main:main']
    }
)
