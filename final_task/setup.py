import setuptools

setuptools.setup(
    name='pycalc',
    version='1.0'
    author='Vlada Garavaya',
    author_email='vl.garavaya@gmail.com',
    packages=find_packages(),
    entry_points={'console_scripts': ['pycalc=pycalc.pycalc:main']},
)
