from setuptools import setup, find_packages

setup(
    name='pycalc',
    version='1.0',
    author='Ilya Kapitonau',
    author_email='ilya.th.kapitonov@gmail.com',
    description='Pure-python command-line calculator.',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pycalc=pycalc.pycalc:main',
        ],
    }
)
