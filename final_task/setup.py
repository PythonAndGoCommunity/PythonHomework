from setuptools import setup, find_packages

setup(
    name='pycalc',
    version='1.0.0',
    author='Gleb Nikitin',
    author_email='nikitin_gleb@tut.byu',
    packages=find_packages(),
    entry_points={'console_scripts': ['pycalc=pycalc.pycalc:main']},
)
