from setuptools import setup, find_packages

setup(
    name='pycalc',
    description='Calculator',
    version='0.1',
    author='UnicornTT',
    author_email='kirill.unicorntt@gmail.com',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pycalc=pycalc.core:main',
        ]
    })
