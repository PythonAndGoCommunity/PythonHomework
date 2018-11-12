from setuptools import setup, find_packages

setup(
    name='pycalc',
    version='0.5',
    author='Vladislav Pirtan',
    author_email='Vpirtan@yandex.ru',
    packages=find_packages(),
    entry_points={'console_scripts': ['pycalc=pycalc.pycalc:main']},
)
