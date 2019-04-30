"""pycalc script setup"""

from setuptools import setup, find_packages  # pragma: no cover

setup(
    name='pycalc',
    version='1.0',
    author='wenaught',
    description='Command-line Python calculator.',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pycalc=pycalc.core:main',
        ]
    })  # pragma: no cover
