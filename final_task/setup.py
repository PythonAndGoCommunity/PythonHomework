from setuptools import setup, find_packages

setup(
    name="Pycalc project",
    version='1.0',
    author="Alexander Gutyra",
    author_email="gutyra13@gmail.com",
    description="Simple pure-Python calculator with custom modules support.",
    packages=find_packages(),
    entry_points={
        'console_scripts': ['pycalc = pycalc.pycalc']
    }
)
