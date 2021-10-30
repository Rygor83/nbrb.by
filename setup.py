#  ------------------------------------------
#   Copyright (c) Rygor. 2021.
#  ------------------------------------------

"""Minimal setup file for tasks project."""

from setuptools import setup, find_packages

setup(
    name='nb',
    version='0.01',
    license='MIT',
    description='Launch sap systems from saplogon with sapshcut.exe',

    author='Rygor',
    author_email='pisemco@gmail.com',
    url='http://rygor.by',

    packages=find_packages(where='src'),
    package_dir={'': 'src'},

    install_requires=['click', 'pandas', ],

    entry_points={
        'console_scripts': [
            'nb = nbrb_by.nbrb_by:cli',
        ]
    },
)
