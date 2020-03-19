#!/usr/bin/env  python3
# -*- coding: utf-8 -*-
import os
import sys


def get_function_name(n=0):
  """
  This simple function will return the function, it's caller, or it's
  caller's caller.

  >>> import zabbix.tools.inspectorgadget
  >>> get_function_name()
  '<module>'
  >>> get_function_name(1)
  '__run'
  >>> get_function_name(2)
  'run'

  :param n: int : indicates the depth of the stack you wish to get;
    0 == Current function
    1 == Current function's caller
    2 == Current function's caller's caller
    ...
  :return: string : function name

  Found at;
    http://stackoverflow.com/questions/5067604/determine-function-name-from-within-that-function-without-using-traceback
  """
  return sys._getframe(n + 1).f_code.co_name


def get_module_name(n=0):
  """
  This simple function will return the file name of the script that
  calls this function.

  >>> import zabbix.tools.inspectorgadget
  >>> get_module_name()
  '<doctest __main__.get_module_name[1]>'
  >>> get_module_name(1)
  'doctest.py'
  >>> get_module_name(2)
  'doctest.py'

  :param n: int : indicates the depth of the stack you wish to get;
    0 == Current function
    1 == Current function's caller
    2 == Current function's caller's caller
    ...
  :return: string : Name of the file that called this function.
  """
  return os.path.basename(sys._getframe(n + 1).f_code.co_filename)


def who_called_us():
  """
  This will attempt to determine if this script was called from the command
  line, cron, or other and adjust the level of output appropriately.  Please
  note that this does not override the debug option, but it does adjust it.

  The return values are;
    0 -- CRONTAB
    1 -- Zabbix (or other script)
    2 -- console / TTY command line

  To help the script distinguish between being called from the Zabbix agent and
  CRON, please set the following environment in the crontab that calls this
  script;
      RUNNING_FROM_CRONTAB

  >>> import zabbix.tools.inspectorgadget
  >>> who_called_us()
  2

  :return int: Verbosity level to use, from zero (quiet) to X (debug)
  """
  if os.isatty(sys.stdin.fileno()):
    return 2

  envkeys = os.environ.keys()
  if 'RUNNING_FROM_ZABBIX' in envkeys:
    return 1

  if 'RUNNING_FROM_CRONTAB' in envkeys:
    return 0

  return 0


if __name__ == '__main__':
  import doctest
  doctest.testmod()
