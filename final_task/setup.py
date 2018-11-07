from setuptools import setup, Extension

setup(
    name='pycalc',
    version='1.0.0',
    description='Pure-python command-line calculator.',
    author='Anastasiya Holubeva',
    author_email='anastasyago@yandex.ru',
    url='https://github.com/hfvh/Pycalc',
    packages=['pycalc'],
    entry_points={
        'console_scripts': [
            'pycalc=pycalc.calc:main',
        ],
    },
)
