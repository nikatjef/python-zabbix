#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is a tool created to help troubleshoot some LLD issues with the MySQL
version of the Zabbix proxy.
"""
import socket
import sys
import time
import zabbix

ZBX_HOST_NOTFOUND = 'Host does not exist in Zabbix.'
ZBX_HOST_NOACTIVE = 'Host does not have any Zabbix agent (active) checks.'
ZBX_HOST_REGISTER = 'Host has been registered.'
ZBX_HOST_DIDEXIST = 'Host already exists.'
ZBX_HOST_UNKNWON  = 'Unable to determine if the host is registerd or not.'

def main():
  print get_ActiveItemList()
  return 0


def get_ActiveItemList(**kwargs):
  def zbx_ask_question(connection, question):
    connection.send(zbxQuestion)
    retval = connection.recv(8192)
    return (len(retval), retval)

  zbxConfig = zabbix.get_AgentConfig(**kwargs)
  if kwargs.get('auto_register', False):
    run_count = int(kwargs.get('run_count', 0))
    run_delay = int(kwargs.get('run_delay', 1))
  else:
    run_count = 0
    run_delay = 1

  count = 0
  size = 0
  zbxQuestion = 'ZBX_GET_ACTIVE_CHECKS\n{0}\n'.format(zbxConfig.zabbix_host)
  zbxClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  while size == 0:
    count += 1
    zbxClient.connect((zbxConfig.zabbix_serv, int(zbxConfig.zabbix_port)))
    (size, content) = zbx_ask_question(zbxClient,zbxQuestion)
    zbxClient.close()
    if count > run_count:
        break
    time.sleep(1)

  if size == 0:
    return ZBX_HOST_NOTFOUND

  if kwargs.get('auto_register', False):
    if size > 8:
      return ZBX_HOST_DIDEXIST
    elif size == 8:
      return ZBX_HOST_REGISTER
    else:
      return ZBX_HOST_UNKNOWN
  
  if size == 8:
    return ZBX_HOST_NOACTIVE

  return [x.rsplit(':',2) for x in content.split('\n') if x != 'ZBX_EOF' and len(x) > 1]

if __name__ == '__main__':
  sys.exit(main())
