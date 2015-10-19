#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple lib to connect to a Zabbix agent and request the value of an item.
"""
def query_agent(**kwargs):
  """
  Open a socket to port 10050 on the remote server and query for the number of
  processes running via proc.num[<FOO>], where FOO is either zabbix_server or
  zabbix_proxy.
  """
  query_string = kwargs.get('query_string', 'agent.ping')

  query_host = kwargs.get('query_host', '127.0.0.1')
  query_port = kwargs.get('query_port', '10050')

  try:
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((query_host, query_port))
  except:
    return (99999, 'ERROR: {} :: {}:{}'.format(e, query_host, query_port))
  else:
    connection.send(query_string)
    result = connection.recv(8192)
    connection.close()

    retval = ''.join(x for x in result if x.isdigit())
    return (0, retval)
  return (0 ,'')


if __name__ == '__main__':
  import doctest
  doctest.testmod()

