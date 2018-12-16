from setuptools import setup

setup(
    name='Calculator',
    version='0.01',
    description='Pure command-line calculator using python',
    author='S.Volodzko',
    url='',
    license='MIT',
    packages=['program'],
    entry_points={'console_scripts': ['pycalc = program.program:main']}
)

'''
You have a package called the program and inside it a file called the program.py
using the main () parameter. Run setup.py like this:

python3 setup.py install

It installed it in the directory of package sites for your platform and will create a console script called a pycalc.
Then you can run the program with your item.
'''
