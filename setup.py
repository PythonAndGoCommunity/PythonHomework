from setuptools import setup

setup(
    name='pycalc',
    version='1.0',
    description='bash python calculator',
    author='obrseh',
    url='epam.com',
    packages=['pycalc'],
    entry_points={'console_scripts': ['pycalc = program.program:main']}
)
