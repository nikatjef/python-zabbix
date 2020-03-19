#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This initializes the zabbix module and provides a few minor tools.
"""
from zabbix.misc import *
from zabbix.getagentconfig import GetAgentConfig
from zabbix.sender import Sender
from zabbix.version import __version__
from zabbix.zlog import zlog,  DEBUG, INFO, WARNING, ERROR, CRITICAL
from zabbix.tools.docopt import docopt

import os
import socket
import time


class Zabbix(object):
  __zabbix_serv_conf__ = '/etc/zabbix/zabbix_server.conf'
  __zabbix_serv_addr__ = 'server1.example.org'
  __zabbix_serv_port__ = 10051

  __zabbix_agnt_conf__ = '/etc/zabbix/zabbix_agentd.conf'
  __zabbix_agnt_addr__ = 'client1.example.org'
  __zabbix_agnt_name__ = socket.gethostname().split('.', 1)[0]
  __zabbix_agnt_port__ = 10050

  __zabbix_node_name__ = socket.getfqdn()

  __zabbix_time_curr__ = int(round(time.time()))

  __script_log_dir__ = '/var/log/zabbix'

  def __init__(self, **kwargs):
    logfile = kwargs.get(
        'logfile',
        os.path.join(
            os.path.expanduser('~'),
            'python-zabbix.log'
            )
        )
    self.logger = ZLog(**kwargs)


__zabbix_serv_conf__ = '/etc/zabbix/zabbix_server.conf'
__zabbix_serv_addr__ = 'server1.example.org'
__zabbix_serv_port__ = 10051

__zabbix_agnt_conf__ = '/etc/zabbix/zabbix_agentd.conf'
__zabbix_agnt_addr__ = 'client1.example.org'
__zabbix_agnt_name__ = socket.gethostname().split('.', 1)[0]
__zabbix_agnt_port__ = 10050

__zabbix_node_name__ = socket.getfqdn()

__zabbix_time_curr__ = int(round(time.time()))


def printvers(caller, version):
  print("{} version: {}".format(__name__, __version__))
  print("{} version: {}".format(caller, version))


if __name__ == '__main__':
  import doctest
  doctest.testmod()
