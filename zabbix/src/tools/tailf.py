#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tail -f in python, truncate aware;
  https://toic.org/blog/2009/tail-f-in-python-truncate-aware/
"""
import time
from os import stat
from os.path import abspath
from stat import ST_SIZE

class LogTail:
  def __init__(self, logfile):
    self.logfile = abspath(logfile)
    self.f = open(self.logfile,"r")
    file_len = stat(self.logfile)[ST_SIZE]
    self.f.seek(file_len)
    self.pos = self.f.tell()

  def _reset(self):
    self.f.close()
    self.f = open(self.logfile, "r")
    self.pos = self.f.tell()

  def tail(self):
    while 1:
      self.pos = self.f.tell()
      line = self.f.readline()
      if not line:
        if stat(self.logfile)[ST_SIZE] < self.pos:
          self._reset()
        else:
          time.sleep(1)
          self.f.seek(self.pos)
      else:
        """print, return or otherwise manipulate the tailed line"""
        print line

