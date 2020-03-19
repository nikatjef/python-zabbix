#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is a pure python replacement for the zabbix_sender tool.
"""
import json
import logging
import re
import socket
import struct
import sys
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

  The class object supports the following keyword arguments at instantiation;
    read_config   -- (Boolean) Tells the class to read default configuration
                     values from the Zabbix agent configuration file. By default
                     the class will attempt to read the configuration file at
                     /etc/zabbix/zabbix_agentd.conf

    zabbix_file   -- (String) This is the Zabbix agent configuration file that
                     should be read to load configuration information from. This
                     is optional and defaults to /etc/zabbix/zabbix_agentd.conf

    zabbix_serv   -- (String) This is the Zabbix server to send monitoring data
                     to. If the class is told to read the configuration, then
                     this value will be take from the 'ServeActive' value from
                     the Zabbix agent configuration file, otherwise it will be
                     set to '127.0.0.1'

    zabbix_host   -- (String) This is the Zabbix client / agent name that the
                     class will send the data as.  If the class is reading from
                     the Zabbix agent configuration file, then this value will
                     be set by the 'Hostname' value from Zabbix agent
                     configuration file, otherwise it will be set to the the
                     hostname of the machine that the script is running on.

    zabbix_port   -- (Integer) This is the port to connect to on the Zabbix
                     server. If the class is reading from the Zabbix agent
                     configuration file, this will be set to the port defined
                     in the 'ServerActive' value from the configuration file,
                     otherwise it will be set to 10051.

    zabbix_time   -- (Integer) This is the current epoch time when the class
                     object is instantiated.  Each item can have a separate time
                     when they are added.


  Usage examples;
    In this example, we are instantiating an object to send monitoring data to a
    server called 'zabbix.example.org'.  The Zabbix server will see the data as
    coming from a host called 'client.example.org', and will show that the data
    was collected when Marty, in the Delorean, left 1985 to go back in in time
    to 1955

      >>> import zabbix
      >>> epochtime1 = 499162920 # 1.21 gigawatts.
      >>> monitor = zabbix.Sender(
      ...   read_config=True,
      ...   zabbix_serv='server1.example.org',
      ...   zabbix_host='client1.example.org',
      ...   zabbix_port=8885,
      ...   zabbix_time=epochtime1
      ...   )
      >>> monitor.zabbix_serv
      'server1.example.org'
      >>> monitor.zabbix_host
      'client1.example.org'
      >>> monitor.zabbix_port
      8885
      >>> monitor.zabbix_time
      499162920

    Please note, that as of this point there has been no communication between
    the node instantiating this object and the Zabbix server.  This is only
    instantiating the object.

    Send one or more items to the Zabbix server.  By default, the sender will
    quietly fail if it connects but sends invalid items. The send function has
    a couple of optional parameters to alter it's behavior;
      print_values -- Boolean to display the items (True) or send them (False)
      iterate_values -- Boolean to send items one at a time (True) or send
      them in bulk.  This defaults to False.
      >>> monitor.send(print_values=True) #doctest: +SKIP
      {'host': 'client1.example.org', 'value': '16535', 'key': 'myKey1', 'clock': 499162920}
      {'host': 'client1.example.org', 'value': '16535', 'key': 'myKey1', 'clock': 499162920}
      {'host': 'client2.example.org', 'value': '16534', 'key': 'myKey1', 'clock': 499162920}
      {'host': 'client3.example.org', 'value': '16533', 'key': 'myKey1', 'clock': 499162920}
  """

  def __init__(self, **kwargs):
    """
    Initialize a new instance of the class.  The class initialization will two
    will instantiate two "private" attributes;
    __list_item__ -- (List) This is the list of item key/value pairs to be sent
                     to the Zabbix server.

    __dict_lld__  -- (Dict) This is a dictionary of low-level discovery objects
                     to send to the Zabbix server.

    While these attributes can be modified directly, it is generally better to
    use the following mutators to get them;
    add_item()    -- (Method) This will add an item key/value pair to the
                     __list_item__ list.

    add_lld()     -- (Method) This will add a discovery object to the dictionary
                     of LLD objects (__dict_lld__).
    """
    logging.debug('Instantiating Zabbix sender')
    self.__list_item__ = []
    self.__dict_lld__ = {}

    logging.debug('Loading Zabbix agent config')
    zbx_config_object = zabbix.GetAgentConfig(**kwargs)
    self.zabbix_host = kwargs.get('zabbix_host', zbx_config_object['zabbix_host'])
    self.zabbix_serv = kwargs.get('zabbix_serv', zbx_config_object['zabbix_serv'])
    self.zabbix_port = kwargs.get('zabbix_port', zbx_config_object['zabbix_port'])
    self.zabbix_time = kwargs.get('zabbix_time', zbx_config_object['zabbix_time'])

    self.verbose = kwargs.get('verbose', False)
    logging.debug('Sender instantiated')

  def __print_values(self, data_set):
    """
    Simple method to print out the Zabbix data instead of sending it to the
    Zabbix server.
    """
    if data_set == 'items':
      dataset = self.__list_item__
    elif data_set == 'lld':
      dataset = self.__dict_lld__
    else:
      dataset = self.__list_item__

    for elem in dataset:
      print(u'{0}'.format(elem))

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
      if len(self.__dict_lld__) == 0:
        obj_data['data'] = {}
      else:
        obj_data['clock'] = self.zabbix_time
        obj_data['data'] = self.__dict_lld__
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
      return 253, err_message

    response_data_header = sock.recv(8)

    response_data_header = response_data_header[:4]
    response_len = struct.unpack('i', response_data_header)[0]
    response_raw = sock.recv(response_len)
    sock.close()
    response = json.loads(response_raw)
    match = re.match(
        r'^.*failed.+?(\d+).*$',
        response['info'].lower() if 'info' in response else ''
        )
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

    Now we are going to add some data that we collected from the Delorean. We do
    this by adding item data to the object we created above. We add the data by
    calling the add_item method.

    The add_item method supports the following arguments;
    key           -- (String) This is the item key that is used by Zabbix to
                     index the data it receives / queries. ** REQUIRED **

    value         -- (String) This is the value to send to the Zabbix for the
                     item defined by the key above. ** REQUIRED **

    clock         -- (Integer) This is the current epoch time when the item is
                     collected. This is optional and will default to the
                     zabbix_time value.

    host          -- (String) This is the Zabbix client / agent name that the
                     class will send this item as. This is optional and will
                     default to the zabbix_host value.

      >>> import zabbix
      >>> epochtime1 = 499162920 # 1.21 gigawatts.
      >>> monitor = zabbix.Sender(
      ...   zabbix_serv='zabbix.example.org',
      ...   zabbix_host='client1.example.org',
      ...   zabbix_port=8885,
      ...   zabbix_time=epochtime1
      ...   )
      >>> monitor.__list_item__
      []

      >>> monitor.add_item(key='myKey1',value='16535')
      True

    This package also supports adding multiple items. Each item must have
    a different key, unless they have different zabbix_host entries.  If you
    use the same key for the same host, it will overwrite the previous item
    value.  This has been tested with 650 items without issue.
      >>> monitor.add_item(key='myKey1',value='16535')
      True
      >>> monitor.add_item(key='myKey1',value='16534',zabbix_host='client2.example.org')
      True
      >>> monitor.add_item(key='myKey1',value='16533',zabbix_host='client3.example.org')
      True

      >>> monitor.__list_item__ == [
      ...   {
      ...     'host': 'client1.example.org',
      ...     'value': '16535',
      ...     'key': 'myKey1',
      ...     'clock': 499162920
      ...   },
      ...   {
      ...     'host': 'client1.example.org',
      ...     'value': '16535',
      ...     'key': 'myKey1',
      ...     'clock': 499162920
      ...   },
      ...   {
      ...     'host': 'client2.example.org',
      ...     'value': '16534',
      ...     'key': 'myKey1',
      ...     'clock': 499162920
      ...   },
      ...   {
      ...     'host': 'client3.example.org',
      ...     'value': '16533',
      ...     'key': 'myKey1',
      ...     'clock': 499162920
      ...   }
      ...   ]
      True

    Please note, that as of this point there has been no communication between
    the node instantiating this object and the Zabbix server.  This is only
    adding item key/value pairs to the list of items to send to the Zabbix
    server.

    @TODO: Fix the add_item to eliminate duplicate host / key tuples.
    """
    if 'key' not in kwargs:
      return False

    if 'value' not in kwargs:
      return False

    obj_data = {
      'host': kwargs.get('zabbix_host', self.zabbix_host),
      'key': kwargs.get('key'),
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
      for item in self.__dict_lld__:
        (retcode, retstring) = self.__send(self.__build_object(build='item'))
        retarray.append((retcode, retstring, item))

    return retarray

  def add_lld(self, **kwargs):
    """
    This will add a Low-Level Discovery (LLD) item to send to the Zabbix server.
    In Zabbix, LLDs provide a mechanism to automatically add items based on
    pre-defined data availability.  A common example of this is the filesystem
    checks on a Unix based system.  We know what data we want to monitor for
    each of the filesystems, but, as server can have their filesystems layed
    out differently from the others, we need a way to tell Zabbix which mount
    point is mounting which filesystem.

    The add_lld method supports the following arguments;
    key           -- (String) This is the item key that is used by Zabbix to
                     index the data it receives / queries. ** REQUIRED **

    entries       -- (List) This is ia list of the MACRO / value pairs used to
                     add LLD items to Zabbix.

    host          -- (String) This is the Zabbix client / agent name that the
                     class will send this item as. This is optional and will
                     default to the zabbix_host value.

    For example, the Delorean has four tires, but they are four completely
    different tires, each with a different optimal tire pressure.  Through the
    use of LLDs, we can tell Zabbix not only what the optimal pressure, as well
    as the manufacturer.
      >>> import zabbix
      >>> epochtime1 = 499162920 # 1.21 gigawatts.
      >>> monitor = zabbix.Sender(
      ...   zabbix_serv='zabbix.example.org',
      ...   zabbix_host='client1.example.org',
      ...   zabbix_port=8885,
      ...   zabbix_time=epochtime1
      ...   )
      >>> monitor.__dict_lld__
      {}

    Add the LLD values for the left tire.
      >>> monitor.add_lld(
      ...   key='tires[front]',
      ...   entries=[
      ...     ('{$LOCATION}', 'LEFT'),
      ...     ('{$OPTIMAL_PRESSURE}', 32),
      ...     ('{$MANUFACTURER}', 'Dunlop')
      ...     ]
      ...   )
      True
      >>> len(monitor.__dict_lld__.keys())
      1

    And now the right tire.  Note that we are using the same key to append this
    new tire to the existing list of tires.
      >>> monitor.add_lld(
      ...   key='tires[front]',
      ...   entries=[
      ...     ('{$LOCATION}', 'RIGHT'),
      ...     ('{$OPTIMAL_PRESSURE}', 40),
      ...     ('{$MANUFACTURER}', 'Pirelli')
      ...     ]
      ...   )
      True
      >>> len(monitor.__dict_lld__.keys())
      1

    And now the rear tires.  Note that we are using a new key to create a new
    LLD item.
      >>> monitor.add_lld(
      ...   key='tires[rear]',
      ...   entries=[
      ...     ('{$LOCATION}', 'RIGHT'),
      ...     ('{$OPTIMAL_PRESSURE}', 36),
      ...     ('{$MANUFACTURER}', 'Hancook')
      ...     ]
      ...   )
      True

      >>> monitor.add_lld(
      ...   key='tires[rear]',
      ...   entries=[
      ...     ('{$LOCATION}', 'LEFT'),
      ...     ('{$OPTIMAL_PRESSURE}', 28),
      ...     ('{$MANUFACTURER}', 'Goodyear')
      ...     ]
      ...   )
      True

      >>> len(monitor.__dict_lld__[('client1.example.org', 'tires[rear]')])
      6

      #>>> monitor.__dict_lld__[('client1.example.org', 'tires[rear]')]

    @TODO: Add support for adding multiple LLD items at the same time
    """
    item = []

    host = kwargs.get('host', self.zabbix_host)
    zkey = kwargs.get('key', False)
    entries = kwargs.get('entries', False)

    lld_host_key = (host, zkey)

    """
    We need to test the inputs to ensure that we have the correct keys
    and the correct value types.
    """
    if not zkey:
      return False

    if not entries:
      self.__dict_lld__[lld_host_key] = item
      return True

    if not isinstance(entries, list):
      return False

    """
    We have valid keys and value types.
    """
    for entry in entries:
      if isinstance(entry, tuple) and len(entry) == 2:
        item.append(entry)
      else:
        continue

    if len(item) == 0:
      return False

    if lld_host_key in self.__dict_lld__:
      tmp_list = self.__dict_lld__[lld_host_key]
#      tmp_list.append(item)
      self.__dict_lld__[lld_host_key] = tmp_list + item
    else:
      self.__dict_lld__[lld_host_key] = item

#    obj_data = {
#      'host':  kwargs.get('zabbix_host', self.zabbix_host),
#      'key':   kwargs.get('key'),
#      'value': item[0] if len(item) == 1 else '[{}]'.format(','.join(item)),
#      }

#    self.__dict_lld__.append({key:obj_data})
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
      for item in self.__dict_lld__:
        (retcode, retstring) = self.__send(self.__build_object(build='lld'))
        retarray.append((retcode, retstring, item))

    return retarray


if __name__ == '__main__':
  import doctest
  doctest.testmod()
