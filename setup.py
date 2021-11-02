#  ------------------------------------------
#   Copyright (c) Rygor. 2021.
#  ------------------------------------------

"""Minimal setup file for tasks project."""

from setuptools import setup, find_packages

setup(
    name='nb',
    version='1.6',
    license='MIT',
    description="CMD. Info about exchange rates established by the National Bank of the Republic of Belarus",

    author='Rygor',
    author_email='pisemco@gmail.com',

    packages=find_packages(where='src'),
    package_dir={'': 'src'},

    install_requires=['click', 'pandas', ],

    entry_points={
        'console_scripts': [
            'nb = nbrb_by.nbrb_by:cli',
        ]
    },
)
