#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This script will query various information from the information_schema database
for MySQL / MariaDB and report the results to Zabbix.

This script is born out of a hybrid of Percona's Zabbix template for MySQL and
MySQL Tuner's reporting.

Percona's Zabbix template uses an external mapping of Zabbix items and MySQL
status names.  Instead this script will use the Zabbix LLD system, as much as
possible, to directly map the MySQL status names to Zabbix items.  In those
cases where Zabbix LLD is not appropriate the script and associated template
will use the status name as defined in MariaDB 10.0.

Additionally, this script, and associated template, will apply some of the
basic sanity checking from MySQL tuner to give a better impression of the
overall health of the MySQL instance. Where appropriate these sanity checks
will be performed by the script with the results being sent to the Zabbix
server.

Finally, this script will also monitor 'On-Disk' DB sizes for all databases,
with the exception of the core MySQL / MariaDB databases (mysql,
information_schema, and performance_schema)
"""
import os
import sys
import zabbix
import zabbix_mysql

from zabbix_mysql import db_size_query

def main(**kwargs):
  mysql_options = read_config_ini(**kwargs)

  foo = db_size_query.main(**mysql_options)
  for x in foo.keys():
    print x
    print
  exit(0)
  
  retval = (0, '')
  verbosity = who_called_us()

  logger = 'foo'
  if verbosity == 1:
    write_log(logger, retval[1])
  elif verbosity == 2:
    write_log(logger, retval[0])
  else:
    pass

  return retval[0]

def who_called_us():
  """
  This will attempt to determine if this script was called from the command
  line, cron, or other and adjust he level of output appropiately.  Please note
  that this does not override the debug option, but it does adjust it.

  To help the script distinguish between being called from the Zabbix agent and
  CRON, please set the following environment in the crontab that calls this
  script;
      RUNNING_FROM_CRONTAB
  """
  if 'RUNNING_FROM_CRONTAB' in os.environ.keys():
    retval = 0
  elif not os.isatty(sys.stdin.fileno()):
    retval = 1
  else:
    retval = 2

  return retval

def write_log(logger, message=''):
  print 'Log entry written to: {}'.format(logger)
  print '  Message was: {}'.format(message)

def read_config_ini(**kwargs):
  from zabbix.tools import parse_file_kvp
  retval = parse_file_kvp.__parse_file_kvp(
      filename=kwargs.get(
          'filename',
          zabbix_mysql.__default_mysql_cnf_file
          ),
      section=kwargs.get(
          'section',
          zabbix_mysql.__default_mysql_cnf_section
          )
      )
  return retval

if __name__ == '__main__':
  sys.exit(main())
