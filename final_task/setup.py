from setuptools import setup, find_packages

setup(name="pycalc",
      version="1.2.1",
      author="Nick Dubovik",
      author_email="kizrumscience@yandex.ru",
      description='A program to calculate complex mathematical expressions with support for custom libraries.',
      scripts={"pycalc.py"},
      packages=find_packages(),
      entry_points={'console_scripts': ['pycalc = pycalc:main']}, )
