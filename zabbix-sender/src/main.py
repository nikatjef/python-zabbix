#!/usr/bin/env python
"""
"""
import sys
import zabbix


def main():
  arguments = parse_arguments()
  monitor = zabbix.Sender(**arguments)
  if 'zabbix_key' in arguments:
    if 'item_file' in arguments:
      print 'Sending failed.  -k and -i cannot be used together.'
      return 1
    if 'zabbix_value' not in arguments:
      print 'Sending failed.  -k requires -o.'
      return 1

    monitor.add_item(key=arguments['zabbix_key'], value=arguments['zabbix_value'])

  if 'item_file' in arguments:
    split_count = 3 if arguments['with_timestamps'] else 2

  retval = monitor.send(print_values=False)
  if arguments['verbose']:
    print retval[0][1]['info']
#    print retval[0][1][0]
  return retval[0][0]


def parse_arguments():
  """
  Collect and collate command line arguments.
  """
  import argparse

  parser = argparse.ArgumentParser(
      add_help=True,
      description="Send one or more key/value pairs to the Zabbix server.",
      )
  parser.add_argument(
      '-V', '--version',
      action='version',
      help='Display version number',
      version='%(prog)s v{}'.format(zabbix.__version__)
      )

  noisey = parser.add_mutually_exclusive_group()
  noisey.add_argument(
      '-v', '--verbose',
      action='count',
      help='Verbose mode, -vv for more details (Disabled)',
      dest='verbose',
      default=0,
      )
  noisey.add_argument(
      '-q', '--quiet',
      action='count',
      help='Disable all output',
      dest='quiet',
      default=0,
      )

  parser.add_argument(
      '-c', '--config',
      action='store',
      help='Absolute path to the configuration file. Default is /etc/zabbix/zabbix_agentd.conf',
      dest='zabbix_agent_conf',
      nargs='?',
      default=argparse.SUPPRESS,
      metavar='<file>',
      )
  parser.add_argument(
      '-z', '--zabbix-server',
      action='store',
      help='Hostname or IP address of Zabbix server',
      dest='zabbix_serv',
      nargs='?',
      default=argparse.SUPPRESS,
      metavar='<server>',
      )
  parser.add_argument(
      '-p', '--port',
      action='store',
      help='Specify port number of server trapper running on the server. Default is {}'.format(zabbix.__zabbix_serv_port__),
      dest='zabbix_port',
      nargs='?',
      default=argparse.SUPPRESS,
      metavar='<server port>',
      type=int,
      )
  parser.add_argument(
      '-s', '--host',
      action='store',
      help='Specify host name. Host IP address and DNS name will not work. Default is {}'.format(zabbix.__zabbix_node_name__),
      dest='zabbix_host',
      nargs='?',
      default=argparse.SUPPRESS,
      metavar='<hostname>',
      )
  parser.add_argument(
      '-I', '--source-address',
      action='store',
      help='Specify source IP address.',
      dest='ip_address',
      nargs='?',
      default=argparse.SUPPRESS,
      metavar='<IP address>',
      )

  sendmode_single = parser.add_argument_group('Single Item')
  sendmode_single.add_argument(
      '-k', '--key',
      action='store',
      help='Specify item key',
      dest='zabbix_key',
      nargs='?',
      default=argparse.SUPPRESS,
      metavar='<key>',
      )
  sendmode_single.add_argument(
      '-o', '--value',
      action='store',
      help='Specify item value',
      dest='zabbix_value',
      nargs='?',
      default=argparse.SUPPRESS,
      metavar='<key value>',
      )
  
  sendmode_multiple = parser.add_argument_group('Multiple Item')
  sendmode_multiple.add_argument(
      '-i', '--input-file',
      action='store',
      help='Load values from input file. To specify standard input, use "-"',
      dest='item_file',
      nargs='?',
      default=argparse.SUPPRESS,
      metavar='<input file>',
      )
  sendmode_multiple.add_argument(
      '-T', '--with-timestamps',
      action='store_true',
      help='Load values from input file. Specify - for standard input. Each line of file contains whitespace delimited: <hostname> <key> <value>. Specify - in <hostname> to use hostname from configuration file or --host argument. All entries are sent in a sequential order top-down.',
      dest='with_timestamps',
      )

  sendmode_realtime = parser.add_argument_group('Real Time Items')
  sendmode_realtime.add_argument(
      '-r', '--real-time',
      action='store_true',
      help='Send values one by one as soon as they are received. This can be used when reading from standard input.',
      dest='real-time',
      )

  cliargs = {key: value for key, value in vars(parser.parse_args()).items() if value is not None}
  cnfargs = vars(zabbix.get_AgentConfig(**cliargs))

  retval = cnfargs.copy()
  retval.update(cliargs)
  return retval

if __name__ == '__main__':
  sys.exit(main())
