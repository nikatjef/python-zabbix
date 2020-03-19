#!/usr/bin/env python3
"""
  Based on script found at;
    http://stackoverflow.com/questions/492519/timeout-on-a-python-function-call

  Simple decorator to wrap a function with a timeout function.  Decorator
  supports the following arguments;
    timeout :: Numeric value representing how long to let the function run
               before stopping it.
    retval  :: The value to return if the function times out.
  >>> @Timeout(timeout=3)
  ... def waste_time(duration=5):
  ...   from time import sleep
  ...   for count in range(1, duration + 1, 1):
  ...     print(count)
  ...     sleep(1)
  ...   return True
  >>> waste_time(duration=2)
  1
  2
  True

  >>> waste_time(duration=65)
  1
  2
  3
  False
"""
import signal


class TimeoutError(Exception):
  pass


def handler(signum, frame):
  raise TimeoutError()


class Timeout(object):

  def __init__(self, timeout=5, timeout_retval=False):
    self.timeout = timeout
    self.timeout_retval = timeout_retval

  def __call__(self, wrapped_function):

    def wrapper(*args, **kwargs):
      old_handler = signal.signal(signal.SIGALRM, handler)

      signal.signal(signal.SIGALRM, handler)
      signal.alarm(self.timeout)
      try:
        retval = wrapped_function(*args, **kwargs)
      except TimeoutError as exc:
        retval = self.timeout_retval
      finally:
        signal.alarm(0)
      signal.signal(signal.SIGALRM, old_handler)
      return retval
    return wrapper


if __name__ == '__main__':
  import doctest
  doctest.testmod()

