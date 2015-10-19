#!/usr/bin/env  python
# -*- coding: utf-8 -*-
import os
import sys

"""
This simple lambda function will return the function, it's caller, or it's
caller's caller.

It accepts a single argument which indicates the depth of the stack you
with to get;
  0 == Current function
  1 == Current function's caller
  2 == Current function's caller's caller
  ...

  Found at;
  http://stackoverflow.com/questions/5067604/determine-function-name-from-within-that-function-without-using-traceback
"""
get_function_name = lambda n=0: sys._getframe(n + 1).f_code.co_name


#"""
#This simple lambda function will return the name of the class where it
#was called from.
#"""
#get_class_name = lambda n: n.__class__.__name__
#get_module_name = lambda: os.path.basename(__file__)

