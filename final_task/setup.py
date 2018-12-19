from setuptools import setup, find_packages

setup(
    name='pycalc',
    version='1.0',
    author='Pavel Kuzmich',
    author_email='pavelkuz99@outlook.com',
    description='Pure Python command-line calculator',
    packages=find_packages(),
    scripts=['calculator/pycalc']
)
