from setuptools import setup

setup(
    name='pycalc',
    version='1.0',
    packages=['pycalc'],
    url='',
    license='',
    author='zavxoz',
    author_email='',
    description='pure-python calculator',
    entry_points={
        'console_scripts': ['pycalc = pycalc.main:main']
    }
)
