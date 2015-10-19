#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Basic linear regression function;
  http://jmduke.com/posts/basic-linear-regressions-in-python/
"""
def basic_linear_regression(x, y):
  """
  Basic computations to save a little time.
  """
  length = len(x)
  sum_x = sum(x)
  sum_y = sum(y)

  """
  Σx^2, and Σxy respectively.
  """
  sum_x_squared = sum(map(lambda a: a * a, x))
  sum_of_products = sum([x[i] * y[i] for i in range(length)])

  """
  Magic formulae!
  """
  a = (sum_of_products - (sum_x * sum_y) / length) / (sum_x_squared - ((sum_x ** 2) / length))
  b = (sum_y - a * sum_x) / length
  return a, b

if __name__ == '__main__':
  sys.exit(0)
