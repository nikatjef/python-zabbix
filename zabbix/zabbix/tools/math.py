#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def calc_mean(x):
  """
  Simple mean value calculation.  Will return False if x is an empty set.

  :param x: list : List of numbers to find the mean average of
  :return: float : Mean average of the numbers in x.  If x is not a list or
                   or an empty set, return False.

  >>> quiz_scores = [
  ...   9, 6, 8, 6,
  ...   7, 9, 8, 5,
  ...   7, 8, 7, 7,
  ...   6, 8, 9, 6,
  ...   6, 6, 5, 7,
  ...   3, 5, 9
  ...   ]
  >>> calc_mean(quiz_scores)
  6.826086956521739

  >>> calc_mean([])
  False
  """
  if x == []:
    return False
  if not isinstance(x, list):
    return False
  return sum(x, 0.0) / len(x)


def calc_deviation(x,y):
  """
  Simple deviation calculation

  :param x: int : Base number to compare with the mean average
  :param x: int : Mean average.
  :return: float : Deviation from mean.

  >>> quiz_scores = [
  ...   9, 6, 8, 6,
  ...   7, 9, 8, 5,
  ...   7, 8, 7, 7,
  ...   6, 8, 9, 6,
  ...   6, 6, 5, 7,
  ...   3, 5, 9
  ...   ]
  >>> mean = calc_mean(quiz_scores)
  >>> [calc_deviation(x, mean) for x in quiz_scores]
  [2.1739130434782608, -0.8260869565217392, 1.1739130434782608, -0.8260869565217392, 0.17391304347826075, 2.1739130434782608, 1.1739130434782608, -1.8260869565217392, 0.17391304347826075, 1.1739130434782608, 0.17391304347826075, 0.17391304347826075, -0.8260869565217392, 1.1739130434782608, 2.1739130434782608, -0.8260869565217392, -0.8260869565217392, -0.8260869565217392, -1.8260869565217392, 0.17391304347826075, -3.8260869565217392, -1.8260869565217392, 2.1739130434782608]

  >>> calc_deviation(mean, mean)
  0.0
  """
  return (x - y)


def calc_standard_deviation(x):
  """
  Simple variance calculation.

  >>> quiz_scores = [
  ...   9, 6, 8, 6,
  ...   7, 9, 8, 5,
  ...   7, 8, 7, 7,
  ...   6, 8, 9, 6,
  ...   6, 6, 5, 7,
  ...   3, 5, 9
  ...   ]
  >>> calc_standard_deviation(quiz_scores)
  1.5223601217401388
  """
  if x == []:
    return False
  if not isinstance(x, list):
    return False

  mean = calc_mean(x)
  variance = calc_mean([calc_deviation(y,mean) ** 2 for y in x])
  return variance ** 0.5


def calc_range(x):
  """
  Simple range.

  >>> calc_range([10, 2, 5, 6, 7, 3, 4])
  8
  """
  if x == []:
    return False
  if not isinstance(x, list):
    return False

  return max(x) - min(x)


def calc_median(x):
  """
 
  >>> quiz_scores = [
  ...   9, 9, 9, 8,
  ...   8, 8, 8, 7,
  ...   7, 7, 7, 7,
  ...   6, 6, 6, 6,
  ...   6, 6, 5, 5,
  ...   1, 2, 5, 5,
  ...   1, 2, 1
  ...   ]
  >>> calc_median(quiz_scores)
  6
  
  """
  if x == []:
    return False
  if not isinstance(x, list):
    return False

  x_sorted = sorted(x)
  y, z = divmod(len(x), 2)
  if x:
    return x_sorted[y]

  return sum(x_sorted[y-1:y+1]) / 2.0


def calc_linear_regression(x, y):
  """
  Basic computations to save a little time. This function was originally based
  on a function I found at;
    http://jmduke.com/posts/basic-linear-regressions-in-python/

  >>> selling_price = [
  ...   245, 312, 279, 308,
  ...   199, 219, 405, 324,
  ...   319, 255
  ...   ]

  >>> size_sq_feet = [
  ...   1400, 1600, 1700, 1875,
  ...   1100, 1550, 2350, 2450,
  ...   1450, 1700
  ...   ]

  >>> calc_linear_regression(selling_price, size_sq_feet)
  (5.3162528182083095, 194.39356758331922)

  >>> x = [ 1, 2, 3, 4, 5 ]
  >>> y = [ 1, 2, 1.3, 3.75, 2.25 ]
  >>> calc_linear_regression(x, y)
  (0.425, 0.7850000000000001)
  """

  len_x = len(x)
  len_y = len(y)
  length = min(len_x, len_y)

  sum_x = sum(x)
  sum_y = sum(y)

  """
  Σx^2
  """
  sum_x_squared = sum([a ** 2 for a in x])

  """
  Σxy
  """
  sum_of_products = sum([x[i] * y[i] for i in range(length)])

  """
  Magic formulae!
  """
  a = (sum_of_products - (sum_x * sum_y) / len_x) / (sum_x_squared - ((sum_x ** 2) / len_x))
  b = (sum_y - a * sum_x) / len_x
  return a, b


if __name__ == '__main__':
  import doctest
  doctest.testmod()
