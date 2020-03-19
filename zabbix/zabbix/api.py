#!/usr/bin/env python3
"""
"""
import hashlib
import json
import logging
import sys


class ZabbixAPIException(Exception):
  """
  Zabbix API exceptions.
  Error Codes:
    -32602 - Invalid Parameters
    -32500 - No Permission
  """
  pass


class AlreadyExists(ZabbixAPIException):
  """
  Parameters already exist.
  """
  pass


class InvalidProtocolError(ZabbixAPIException):
  """
  Recieved an invalid protocol request.
  """
  pass


class APITimeout(ZabbixAPIException):
  """
  HTTP(s) request timed out.
  """
  pass


class ZabbixAPI(object):
  """
  """
  zabbix = {}

  method = None
  params = {}

  timeout = 10

  id = None

  def __init__(self, **kwargs):
    """
    """
    self.log_level = kwargs.get('log_level', logging.WARNING)
    self.logger = logging.StreamHandler(sys.stdout)

    self.timeout = kwargs.get('timeout', 10)

    self.zabbix['host'] = kwargs.get('zabbix_host', 'localhost')
    self.zabbix['http'] = kwargs.get('zabbix_http', 'http://localhost/zabbix')
    self.zabbix['path'] = kwargs.get('zabbix_path', '/api_jsonrpc.php')
    self.zabbix['port'] = kwargs.get('zabbix_port', 80)
    self.zabbix['user'] = kwargs.get('zabbix_user', 'admin')
    self.zabbix['pass'] = "md5({})".format(
        hashlib.md5(
            kwargs.get('zabbix_pass', 'zabbix').encode('utf-8')
            ).hexdigest()
        )

    self.debug(self.log_level, "url: {}".format(self.zabbix['http']))

#    print self.zabbix['pass']

  def debug(self, log_level="info", var="", msg=None):
    """
    """
    log_entry = "{}: {} {}".format(log_level, var, msg)
    self.logger.log(log_level, log_entry)

  def json_obj(self, method, params={}, auth=True):
    """
    """
    obj = {
        'jsonrpc': '2.0',
        'method': method,
        'params': params,
        'id': self.id
        }
    if auth:
      obj['auth'] = self.auth

    return json.dumps(obj)

  def login(self, **kwargs):
    """
    """
    auth_obj = self.json_obj(
        'usr.login',
        { 'user': self.zabbix['user'], 'password': self.zabbix['pass'] },
        auth=False
        )

    self.debug(logging.DEBUG,auth_obj)


if __name__ == '__main__':
  foo = ZabbixAPI()
  foo.login()
