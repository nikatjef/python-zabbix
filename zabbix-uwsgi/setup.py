#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Basic setup.py file for Python setuptools
python setup.py install

python setup.py test

python setup.py develop

Copyright (c) 2015, James Wells
All rights reserved.
"""
import os
from setuptools import setup

AUTHOR_NAME = "James Wells"
AUTHOR_MAIL = "jwells@dragonheim.net"

__BASE_NAME = os.path.basename(__file__)
__WORK_PATH = os.path.dirname(os.path.realpath(__file__))
__PACK_NAME = __WORK_PATH.rsplit('/', 1)[-1]

__PACK_NAME_MOD = __PACK_NAME.replace('python-', '')
__PACK_NAME_MOD_UNDERSCORE = __PACK_NAME_MOD.replace('-', '_')

__PACK_URL = 'http://github.com/nikatjef/{}'.format(__PACK_NAME)

with open('src/version.py') as f: exec(f.read())

ENTRY_POINTS = {
    'console_scripts': [
        'zabbix-mysql=main:main'.format(__PACK_NAME_MOD),
        ]
    }

setup(
  name='python-' + __PACK_NAME,
  license='GPLv2',
  url=__PACK_URL,
  author=AUTHOR_NAME,
  author_email=AUTHOR_MAIL,
  version=__version__,
  description="Simple pure-python replacement for the Percona MySQL Zabbix monitors.",
  package_dir={'zabbix_mysql': 'src'},
  packages=['zabbix_mysql'],
  zip_safe=False,
  install_requires=[
      "python-zabbix=={}".format(__version__),
      "PyMySQL==0.6.7",
      ],
  entry_points=ENTRY_POINTS,
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
      ],
  )
