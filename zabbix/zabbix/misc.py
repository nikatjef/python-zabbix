#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This initializes the zabbix module and provides a few minor tools.
"""


def __gen_zabbix_key(container, *args):
  """
  Simple tool to generate Zabbix item keys.

  This tool will generate item keys based on the arguments passed.
  The first argument passed will be treated as the primary key, while
  all subsequent arguments will be treated as arguments to to the
  primary key.  For example;
    >>> import zabbix
    >>> zabbix.misc.__gen_zabbix_key('box','red','wagon')
    'box[red,wagon]'

  This tool does require at least a single argument, which is used as
  the primary key.  If no further arguments are passed, the tool will
  return just the single argument;
    >>> zabbix.misc.__gen_zabbix_key('box')
    'box'
  """
  if len(args) == 0:
    return container

  return '{}[{}]'.format(container, ','.join(args))


def __query_rest_service(**kwargs):
  """
  Simple function to query rest services. It's not real efficient, but I
  found myself using the same code snippet over and over again.
  """
  import json
  import requests

  from requests.auth import HTTPBasicAuth

  service_scheme = kwargs.get('scheme', 'http')
  service_host = kwargs.get('host', '127.0.0.1')
  service_port = kwargs.get('port', '80')
  service_path = kwargs.get('path', 'api')

  service_user = kwargs.get('username', False)
  service_pass = kwargs.get('password', False)

  service_verify = kwargs.get('ssl_verify', None)

  service_url = '{}://{}:{}/{}'.format(
      service_scheme,
      service_host,
      service_port,
      service_path
      )

  service_request = requests.get(
      url=service_url,
      verify=service_verify,
      auth=HTTPBasicAuth(
        service_user,
        service_pass
        )
      )

  print(service_request.text)
  data_type = kwargs.get('data_type', 'json')
  if data_type == 'json':
    retval = json.loads(service_request.text)
  elif data_type == 'html':
    retval = json.loads(service_request.text)
  else:
    retval = json.loads(service_request.text)

  return retval


def version_compare(ver_string_a, ver_string_b):
  """
  Simple function to normalize the standard notation version strings
  and compare them.
  """
  import re

  def normalize(version):
    """
    This will normalize the values.
    """
    return [int(x) for x in re.sub(r'(\.0+)*$', '', version).split(".")]

  return cmp(normalize(ver_string_a), normalize(ver_string_b))


def flatten(d, parent_key='', sep='_'):
  import collections
  items = []
  for k, v in d.items():
    new_key = parent_key + sep + k if parent_key else k
    if isinstance(v, collections.MutableMapping):
      items.extend(flatten(v, new_key, sep=sep).items())
    else:
      items.append((new_key, v))
  return dict(items)

