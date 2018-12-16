from setuptools import setup, find_packages

setup(
    name="Calculator",
    author="Andrey Mirugin",
    version="1.0",
    author_email="andrey.mirugin@gmail.com",
    description=("Pure-python command-line calculator."),
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pycalc = pycalc.pycalc:main',
        ]
    }
)

