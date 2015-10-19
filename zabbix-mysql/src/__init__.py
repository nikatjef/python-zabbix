#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This initializes the zabbix-mysql package with a couple simple defaults.
"""
from .version import __version__
from .db_size_query import *

__default_mysql_cnf_file = '/etc/mysql/zabMon.cnf'
__default_mysql_cnf_section = 'zabMon'
