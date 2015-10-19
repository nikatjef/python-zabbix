#!/usr/bin/env python
# -*- coding: utf-8 -*-

import zabbix
import zabbix.tools
from zabbix.tools import parse_file

def GetAgentConfig(**kwargs):
  """
  This simple module will consume the Zabbix agent configuration file and
  return it as dictionary.  Additionally, if needed the whole configuration
  file is available, but not processed.

  When this script consumes the Zabbix agent configuration file, it will
  look at these three variables;
      Hostname -- Available as zabbix_host attribute.  If this variable is not
        set in the configuration file, the attribute will be set to the FQDN
        (if available) of this host.
      ServerActive -- Available as zabbix_serv and zabbix_port attributes. If
        this variable is not set, it will attempt to use the first memeber of 
        the Sever variable.
      Server -- Will be available as zabbix_serv and zabbix_port in the event
        that ServerActive is blank, and even then, it will only return the
        first member of the list.

  The Zabbix spcification for the Server and ServerActive variales allow for
  zero or more entries, with or without port assignments using colons (:) to
  separate the hostname / address from the port.

  When the Zabbix agent starts up, if it is configured to enable active item
  checks, it will contact each of the servers listed in the ServerActivegentConfiG
  variable and ask them for a list of things to monitor. It will then send
  those check values to the server that provided the list at the interval 
  specified.

  This module is not that smart.  Instead it only cares about the first one
  listed in either ServerActive (preferred) or Server (if ServerActive not
  defined).  Additionally, at this time, it does not support parsing of IPv6
  so if you are using the IPv6 address shorthand, this module will likely
  return invalid values for zabbix_port.

  Additionally, the entirity of the Zabbix agent configuration file can be 
  accessed as a dict() attribute called zabbix_conf. There is no processing
  performed on this data.

  Finally, the class accepts the following keyword arguments, which will
  override the default values;
    zabbix_agent_conf -- This will tell the class where to find the agent
      configuration file.  It defaults to /etc/zabbix/zabbix_agentd.conf
    zabbix_host -- This is the hostname that the Zabbix server will use for
      storing / processing the data that is sent. If defined, it will
      override the Hostname and HostnameItem values.
    zabbix_serv -- This is the hostname / address of the server to send the
      data to.  If defined, it will override the Server / ServerActive
      values from the configuration file.  Please note that it does not
      support port number assignments.
    zabbix_port -- This is the port to connect to on the Zabbix server and
      will override the values from Server / ServerActive values. If the 
      port is not defined in the configuration file, the Zabbix default port
      (10051) will be used.
    zabbix_time -- This is the current time, in epoch format, when the
      Zabbix package was imported.  This value can also be overriden on a
      per item basis.
  """
  _parse_host_entry = lambda x: x.split(',')[0].split(':')

#  def parse_kvp_file(**kwargs):
#    def __read_file(**kwargs):
#      should_filter = lambda x,y: x.lstrip().startswith(y) or x == ''
#      import os
#      retval = []
#
#      filter_by = kwargs.get('filter_by', ('#',';'))
#
#      file = kwargs.get(
#          'zabbix_agent_conf',
#          zabbix.__zabbix_agnt_conf__
#          )
#      if not os.access(file, os.R_OK):
#        return retval
#
#      with open(file, 'r') as f:
#        retval = [x for x in f if not should_filter(x,filter_by)]
#
#      return retval
#
#    retval = {}
#    options = {}
#    for line in __read_file(**kwargs):
#      if '#' in line:
#        line = line.split('#', 1)[0]
#      if '=' in line:
#        option, value = line.split('=', 1)
#        option = option.strip()
#        value = value.strip()
#        options[option] = value
#    return options

  retval = {}
  if not kwargs.get('read_config', True):
    retval['zabbix_host'] = zabbix.__zabbix_node_name__
    retval['zabbix_serv'] = zabbix.__zabbix_serv_addr__
    retval['zabbix_port'] = int(zabbix.__zabbix_serv_port__)
    retval['zabbix_time'] = int(zabbix.__zabbix_time_curr__)
    retval['zabbix_conf'] = {}
    return retval

  retval['zabbix_conf'] = parse_file.parse_file_kvp(
      filename = kwargs.get(
          'zabbix_agent_conf',
          zabbix.__zabbix_agnt_conf__
          )
      )

  retval['zabbix_host'] = _parse_host_entry(
      kwargs.get(
          'zabbix_host', 
          retval['zabbix_conf'].get(
              'Hostname', 
              zabbix.__zabbix_node_name__
              )
          )
      )[0]

  zabbix_serv = _parse_host_entry(
      kwargs.get(
          'zabbix_serv', 
          retval['zabbix_conf'].get(
              'ServerActive', 
               retval['zabbix_conf'].get(
                   'Server',
                   zabbix.__zabbix_serv_addr__
                   )
              )
          ),
      )
  retval['zabbix_serv'] = zabbix_serv[0]
  if len(zabbix_serv) == 1:
    retval['zabbix_port'] = int(zabbix.__zabbix_serv_port__)
  else:
    retval['zabbix_port'] = int(zabbix_serv[1])

  retval['zabbix_time'] = int(kwargs.get('zabbix_time', zabbix.__zabbix_time_curr__))

  return retval

if __name__ == '__main__':
  import doctest
  doctest.testmod()

