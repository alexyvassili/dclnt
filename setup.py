#!/usr/bin/env python

from distutils.core import setup

setup(
    name='Dclnt',
    version=0.2,
    url='https://github.com/',
    license='MIT',
    author='Dclnt Community',
    author_email='escantor@gmail.com',
    description='A library for word-statistic in python modules',
    long_description="",
    packages=['dclnt'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'nltk>=3.2',
        'function-pipe>=1.0',
    ],

    classifiers=[

    ],
)