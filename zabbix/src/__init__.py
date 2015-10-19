#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This initializes the zabbix module and provides a few minor tools.
"""
from .version import __version__
from .misc import *
from .sender import Sender
from .getagentconfig import GetAgentConfig

import socket
import time

__zabbix_serv_conf__ = '/etc/zabbix/zabbix_server.conf'
__zabbix_serv_addr__ = '127.0.0.1'
__zabbix_serv_port__ = 10051

__zabbix_agnt_conf__ = '/etc/zabbix/zabbix_agentd.conf'
__zabbix_agnt_addr__ = 'Zabbix server'
__zabbix_agnt_port__ = 10050

__zabbix_node_name__ = socket.getfqdn()

__zabbix_time_curr__ = int(round(time.time()))
