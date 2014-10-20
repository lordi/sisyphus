#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import os.path
import subprocess
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
# Have to do this after importing setuptools, which monkey patches distutils.
from distutils.extension import Extension

version = '0.1.5'

try:
    long_description = open('README.md', 'rt').read()
except IOError, e:
    long_description = None

setup(
    name='sis',
    version=version,
    description="Sisyphus command runner",
    long_description=long_description,
    license='MIT',
    author='Hannes Gräuler',
    author_email='hgraeule@uos.de',
    download_url='https://github.com/lordi/sisyphus/tarball/v' + version,
    url='http://github.com/lordi/sisyphus',
    packages=['sis'],
    package_dir={'sis': 'src/sis'},
    scripts=['scripts/sis'],
    install_requires=['pyinotify', 'futures'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
)
