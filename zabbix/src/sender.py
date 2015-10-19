#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is a pure python replacement for the zabbix_sender tool.
"""
import json
import re
import socket
import struct
import sys
import time
import zabbix

class Sender(object):
  """
  This class is based on the ZSend class created by Rob Cherry, which was
  based on Enrico Troger's Zabbix sender script, though it has been heavily
  modified and expanded upon.

  The original script can be found at:
      https://www.zabbix.com/forum/showthread.php?p=90132

  The original ZSend class can be found at;
      https://www.zabbix.com/forum/showthread.php?t=40558
  
  Usage examples;
    Instantiate a monitor object.  The Monitor object has the following
    objects, all of which can be overriden by passing them as keyword
    arguments / parameters;
      zabbix_host -- This is the hostname of the Zabbix client / agent.
      zabbix_serv -- This is the hostname of the Zabbix server to send to.
      zabbix_port -- This is the port to connect to on the Zabbix server.
      zabbix_time -- This is the current time in seconds (epoch time).

    It also supports;
      read_config -- Boolean to tell it to read the zabbix agent configouration
      file.  Defaults to true.

      >>> import zabbix
      >>> monitor = zabbix.Sender()

    Add an item to be sent to the Zabbix server. At a minimum, add_item
    requires a key and a value;
      key -- This the Key used by zabbix to contain the item value.
      value -- This is the value to store / evaluate.
      clock -- This defaults to the value of zabbix_time above.
      zabbix_host -- This defaults to the value of zabbix_host above.
      >>> monitor.add_item(key='myKey1',value='16535')
      True

    This package also supports adding multiple items. Each item must have
    a different key, unless they have different zabbix_host entries.  If you
    use the same key for the same host, it will overwrite the previous item
    value.  This has been tested with 650 items without issue.
      >>> monitor.add_item(key='myKey1',value='16539')
      True
      >>> monitor.add_item(key='myKey1',value='16534',zabbix_host='host2')
      True
      >>> monitor.add_item(key='myKey1',value='16533',zabbix_host='host3')
      True

    Send one or more items to the Zabbix server.  By default, the sender will
    quietly fail if it connects but sends invalid items. The send function has
    a couple of optional parameters to alter it's behavior;
      print_values -- Boolean to display the items (True) or send them (False)
      iterate_values -- Boolean to send items one at a time (True) or send
      them in bulk.  This defaults to False.
      >>> monitor.send(print_values=True) #doctest: +ELLIPSIS
      {'host': '...', 'value': '16535', 'key': 'myKey1', 'clock': ...}
      {'host': '...', 'value': '16539', 'key': 'myKey1', 'clock': ...}
      {'host': 'host2', 'value': '16534', 'key': 'myKey1', 'clock': ...}
      {'host': 'host3', 'value': '16533', 'key': 'myKey1', 'clock': ...}
  """

  def __init__(self, **kwargs):
    """
    Initialize a new instance of the class.  The class contains two "private"
    list attributes and four public attributes.

    While python does allow you to modify "private" attributes outside of
    setters / mutators, it is not recommended as it may cause unforseen issues.
    The setters / mutators for these attributes are;
      add_item() -- Adds a single item to the list to be sent to Zabbix.
      add_lld()  -- Adds a single instance of an LLD definition.

    The "private" list attributes are;
      __list_item__ -- This list contains one or more items to be sent
      __list_lld    -- This list contains one or more LLD definitions

      >>> import zabbix
      >>> monitor = zabbix.Sender(zabbix_host='client.example.org')
      >>> monitor.__list_item__
      []

    These two public attributes are set at class initialization time. They can
    also be set / updated directly and will affect the entire sender process;
      zabbix_serv -- This is the hostname of the Zabbix server to send to.
      zabbix_port -- This is the port to connect to on the Zabbix server.

      >>> monitor.zabbix_serv #doctest: +SKIP
      '127.0.0.1'
      >>> monitor.zabbix_port
      10051

    These two public attributes are also set at class iitialization time, but
    they are only used as defaults to the add_item() and add_lld() functions.
    Please note that you can also set / update these attributes directly, but
    doing so will only affect new item / lld entries after the update.
    Additionally, these attributes can be overriden in the add_item and add_lld
    function calls but only for that particular item or lld entry being added.
      zabbix_host -- This is the hostname of the Zabbix client / agent.
      zabbix_time -- This is the time in seconds of when the script started.

      >>> monitor.zabbix_host
      'client.example.org'
      >>> monitor.add_item(key='myKey1',value='16539')
      True
      >>> monitor.__list_item__ #doctest: +ELLIPSIS
      [{'host': 'client.example.org', 'value': '16539', 'key': 'myKey1', 'clock': ...}]
      >>> monitor.zabbix_host = 'Zabbix server'
      >>> monitor.zabbix_host
      'Zabbix server'
      >>> monitor.add_item(key='myKey1',value='16539')
      True
      >>> monitor.__list_item__ #doctest: +SKIP
      [{'host': 'Client.example.org', 'value': '16539', 'key': 'myKey1', 'clock': ...}, {'host': 'Zabbix server', 'value': '16539', 'key': 'myKey1', 'clock': ...}]

      >>> monitor.zabbix_time #doctest: +SKIP
      1439395414
    """
    self.__list_item__ = []
    self.__list_lld__ = []

    zbx_config_object = zabbix.GetAgentConfig(**kwargs)
    self.zabbix_host = zbx_config_object['zabbix_host']
    self.zabbix_serv = zbx_config_object['zabbix_serv']
    self.zabbix_port = zbx_config_object['zabbix_port']
    self.zabbix_time = zbx_config_object['zabbix_time']

    self.verbose = kwargs.get('verbose', False)

  def __print_values(self,data_set):
    """
    Simple method to print out the Zabbix data instead of sending it to the
    Zabbix server.
    """
    if data_set == 'items':
      dataset = self.__list_item__
    elif data_set == 'lld':
      dataset = self.__list_lld__
    else:
      dataset = self.__list_item__

    for elem in dataset:
      print u'{0}'.format(elem)


  def __build_object(self, **kwargs):
    """
    This will convert the item object to a Zabbix JSON structure for uploading
    to the Zabbix server.
    """
    obj_data = {
      'request': 'sender data',
      'data': [],
      }

    buildwhat = kwargs.get('build', 'item')
    if buildwhat == 'lld':
      if len(self.__list_lld__) == 0:
        obj_data['data'] = {}
      else:
        obj_data['clock'] = self.zabbix_time
        obj_data['data'] = self.__list_lld__
    else:
      if len(self.__list_item__) == 0:
        obj_data['data'] = {}
      else:
        obj_data['clock'] = self.zabbix_time
        obj_data['data'] = self.__list_item__

    return json.dumps(obj_data)

  def __send(self, mydata):
    """
    This method is the real send function, however, it requires that
    the data already be cooked, as such it is recommended that the 'send'
    method be used instead and it will call this private method.
    """
    socket.setdefaulttimeout(5)
    data_length = len(mydata)
    data_header = '{0}{1}'.format(struct.pack('i', data_length), '\0\0\0\0')
    data_to_send = 'ZBXD\1{0}{1}'.format(data_header, mydata)

    try:
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      sock.connect((self.zabbix_serv, self.zabbix_port))
    except Exception as err:
      err_message = u'Error talking to server: {0}\n'.format(err)
      sys.stderr.write(err_message)
      return 255, err_message
    else:
      sock.send(data_to_send)

    try:
      response_header = sock.recv(5)
    except Exception as err:
      err_message = u'Error talking to server: {0}\n'.format(err)
      sys.stderr.write(err_message)
      return 254, err_message

    if not response_header == 'ZBXD\1':
      err_message = u'Invalid response from server. Malformed data?\n---\n{0}\n---\n'.format(mydata)
#      sys.stderr.write(err_message)
      return 253, err_message

    response_data_header = sock.recv(8)

    response_data_header = response_data_header[:4]
    response_len = struct.unpack('i', response_data_header)[0]
    response_raw = sock.recv(response_len)
    sock.close()
    response = json.loads(response_raw)
    match = re.match(r'^.*failed.+?(\d+).*$', response['info'].lower() if 'info' in response else '')
    if match is None:
      err_message = u'Unable to parse server response - \n{0}\n'.format(response)
      sys.stderr.write(err_message)
      return 2, response
    else:
      fails = int(match.group(1))
      if fails > 0:
        if self.verbose is True:
          err_message = u'Failures reported by zabbix when sending:\n{0}\n'.format(mydata)
          sys.stderr.write(err_message)
        return 1, response
      return 0, response

  def add_item(self, **kwargs):
    """
    This will add an item to the Zabbix item object.  We will use the same
    object structure for single or multiple items.

    """
    if 'key' not in kwargs:
      return False

    if 'value' not in kwargs:
      return False

    obj_data = {
      'host':  kwargs.get('zabbix_host', self.zabbix_host),
      'key':   kwargs.get('key'),
      'value': kwargs.get('value'),
      'clock': kwargs.get('clock', self.zabbix_time)
      }

    self.__list_item__.append(obj_data)
    return True

  def send(self, **kwargs):
    """
    This function will determine the proper way to send the values to the
    Zabbix server, or print if 'print_values' is specified.
    """
    print_values = kwargs.get('print_values', False)
    iterate_values = kwargs.get('iterate_values', False)

    if print_values:
      self.__print_values('items')
      # return (1, u'No items to send to the server.\n', '')
      return

    retarray = []
    if not iterate_values:
      (retcode, retstring) = self.__send(self.__build_object(build='item'))
      retarray.append((retcode, retstring))
    else:
      for item in self.__list_lld__:
        (retcode, retstring) = self.__send(self.__build_object(build='item'))
        retarray.append((retcode, retstring, item))

    return retarray

  def add_lld(self, **kwargs):
    """
    This will eventually provide a function that adds Zabbix Low-Level
    Discovery (LLD). In Zabbix LLDs provide a mechanism to automatically
    add items based on specific criteria.
    """
    item = []

    host = kwargs.get('zabbix_host', self.zabbix_host)
    key = kwargs.get('key', False)
    entries = kwargs.get('entries', False)

    if not key or not entries or not isinstance(entries, list):
      return False

    for entry in entries:
      if isinstance(entry,tuple) and len(entry) == 2:
        item.append('{"{#%s}":"%s"}' % (entry))

    if len(item) == 0:
      return False

    if (host, key) not in self.__list_lld__:
      self.__list_lld__.append({(host, key): item})
    else:
      pass

#    obj_data = {
#      'host':  kwargs.get('zabbix_host', self.zabbix_host),
#      'key':   kwargs.get('key'),
#      'value': item[0] if len(item) == 1 else '[{}]'.format(','.join(item)),
#      }

#    self.__list_lld__.append({key:obj_data})
    return True

  def send_lld(self, **kwargs):
    """
    This function will send the LLD data to the Zabbix server / proxy.
    """
    print_values = kwargs.get('print_values', False)
    iterate_values = kwargs.get('iterate_values', False)

    if print_values:
      self.__print_values('lld')
      return (1, u'No items to send to the server.\n', '')

    retarray = []
    if not iterate_values:
      (retcode, retstring) = self.__send(self.__build_object(build='lld'))
      retarray.append((retcode, retstring))
    else:
      for item in self.__list_lld__:
        (retcode, retstring) = self.__send(self.__build_object(build='lld'))
        retarray.append((retcode, retstring, item))

    return retarray

if __name__ == '__main__':
  import doctest
  doctest.testmod()
