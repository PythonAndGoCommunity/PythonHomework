from setuptools import setup, find_packages


setup(
    name="pycalc",
    version="1.0",
    description="Pure-python command-line calculator.",
    author="Mikhailov Anton",
    author_email="delta.99@mail.ru",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pycalc = pycalc.py:main'
        ]
    }
)
