from setuptools import setup, find_packages

setup(name='pycalc',
      version='0.1',
      description='Pure-python command-line calculator.',
      long_description='Really, my python calculator.',
      packages=find_packages(),
      entry_points={
            'console_scripts': ['pycalc = pycalc:calculate']
      }
      )
