from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='pycalc',
    version='1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts':
            ['pycalc = pycalc.pycalc:main']
        },
)
