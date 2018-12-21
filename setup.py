from setuptools import setup, find_packages

setup(
    name="pycalc",
    version="0.1",
    packages=find_packages(),
    scripts=['pycalc.py'],
    author="Veronika Zakharchenia ",
    author_email="zaharchenya.veronik@gmail.com",
    description="Pure-python command-line calculator.",

    entry_points={
        'console_scripts': [
            'pycalc = pycalc:main',
        ]
    },
)


