# -*- coding: utf-8 -*-
import logging
import os
import subprocess
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
# Have to do this after importing setuptools, which monkey patches distutils.
from distutils.extension import Extension

logging.basicConfig()
log = logging.getLogger()

version = '0.1.0'

setup(
    name='sis',
    version=version,
    requires_python='>=2.6',
    description="Sisyphus command runner",
    license='BSD',
    author='Hannes Gräuler',
    author_email='hgraeule@uos.de',
    url='http://github.com/lordi/sisyphus',
    packages=['sis'],
    package_dir={'sis': 'src/sis'},
    scripts=['scripts/sis'],
    install_requires='pyinotify',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
)
