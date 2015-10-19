#!/usr/bin/env python
"""
Based on script found at;
  http://stackoverflow.com/questions/492519/timeout-on-a-python-function-call
"""
def timeout(func, args=(), kwargs={}, timeout_duration=1, default=None):
  import signal

  class TimeoutError(Exception):
    pass

  def handler(signum, frame):
    raise TimeoutError()

  # Grab existing handler
  old_handler = signal.signal(signal.SIGALRM, handler) 
  # set the timeout handler
  signal.signal(signal.SIGALRM, handler) 
  signal.alarm(timeout_duration)
  try:
    result = func(*args, **kwargs)
  except TimeoutError as exc:
    result = default
  finally:
    signal.alarm(0)

  signal.signal(signal.SIGALRM, old_handler) 
  return result

