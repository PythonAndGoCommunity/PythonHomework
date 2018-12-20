from setuptools import setup, find_packages

setup(
      name='pycalc',
      version='1.0',
      packages=find_packages(),
      __version__='1.0',
      entry_points={
      'console_scripts': ['pycalc = pycalc.pycalc:main', ]
      },
      )
