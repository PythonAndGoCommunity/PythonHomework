import setuptools

setuptools.setup(
    name='pycalc',
    version='1.0',
    author='alyohea',
    description='python calculator',
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'pycalc=pycalc.__main__:main'
        ]
    })
