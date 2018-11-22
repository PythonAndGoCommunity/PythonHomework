from setuptools import setup, find_packages

setup(
        name='pycalc',
        version='0.2',
        description='Decide different expressions',
        long_description='No fake',
        classifiers=[
            'Development Status :: Beta test',
            'License :: None :: None',
            'Programming Language :: Python :: 3.6',
        ],
        keywords='calculator',
        url='not add',
        author='Efi-fi',
        author_email='efimprostopro@gmail.com',
        license='None',
        packages=find_packages(),
        install_requires=[],
        include_package_data=True,
        zip_safe=False,
        entry_points={
            'console_scripts':
                ['pycalc = calc.main:main']
        }
      )
