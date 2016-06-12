#!/usr/bin/env python

import os
import sys
from codecs import open
from tickets import __version__
from setuptools import setup, find_packages


def read(f):
    return open(f, encoding='utf-8').read()

argv = sys.argv[-1]

# register
if argv == 'reg':
    os.system('python setup.py register')
    exit()

# publish
if argv == 'pub':
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    exit()

setup(
    name='tickets',
    version=__version__,
    description='Train tickets query via command line.',
    long_description=read('README.rst') + '\n\n' + read('CHANGES'),
    author='protream',
    author_email='protream@gmail.com',
    url='https://github.com/protream/tickets',
    packages=['tickets'],
    py_modules=['tickets'],
    include_package_data=True,
    platforms='any',
    install_requires=[
        'docopt',
        'prettytable',
        'requests>=2.4.3'
    ],
    entry_points={
        'console_scripts': ['tickets=tickets.core:cli']
    },
    license='MIT',
    zip_safe=False,
)
