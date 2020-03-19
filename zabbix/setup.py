#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Basic setup.py file for Python setuptools
python setup.py install

python setup.py test

python setup.py develop
"""
from os.path import dirname, realpath, basename
from setuptools import setup, find_packages

AUTHOR_NAME = "James Wells"
AUTHOR_MAIL = "jwells@dragonheim.net"

__PACK_NAME = basename(dirname(realpath(__file__)))
__PACK_NAME_MOD = __PACK_NAME.replace('-', '_')

__PACK_URL = 'http://github.com/nikatjef/python-zabbix'

with open('zabbix/version.py'.format(__PACK_NAME_MOD)) as f: exec(f.read())

setup(
  name='python-{}'.format(__PACK_NAME),
  license='GPLv2',
  url=__PACK_URL,
  author=AUTHOR_NAME,
  author_email=AUTHOR_MAIL,
  version=__version__,
  description='Simple pure-python Zabbix sender.',
  packages=find_packages(),
  zip_safe=False,
  install_requires=[
    "docopt==0.6.2",
    ],
  classifiers=[
      "Development Status :: 2 - Pre-Alpha",
      "Environment :: Console"
      "Intended Audience :: Information Technology",
      "Intended Audience :: System Administrators",
      "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
      "Programming Language :: Python :: 2.7",
      "Topic :: System :: Monitoring",
      "Topic :: System :: Networking :: Monitoring",
      "Topic :: Utilities",
      ]
  )
