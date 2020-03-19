#!/usr/bin/env python3
"""
"""


def __read_file(**kwargs):
  import os
  should_filter = lambda x,y: x.lstrip().startswith(y) or x == ''

  filename = kwargs.get('filename', '/dev/null')
  filter_by = kwargs.get('filter_by', ('#', ';'))

  retval = []
  if os.access(filename, os.R_OK):
    with open(filename, 'r') as f:
        retval = [x.rstrip('\n') for x in f if not should_filter(x, filter_by)]

  return retval


# def parse_file_yaml(**kwargs):
#   import yaml
#   retval = yaml.load('\n'.join(__read_file(**kwargs)))
#   return retval


def parse_file_kvp(**kwargs):
  retval = {}
  for line in __read_file(**kwargs):
    if '#' in line:
      line = line.split('#', 1)[0]
    if '=' in line:
      option, value = line.split('=', 1)
      option = option.strip()
      value = value.strip()
      retval[option] = value
  return retval


if __name__ == '__main__':
  import doctest
  doctest.testmod()

