"""
This module is responsible for operating with piped input.
It has only one function Get.
"""
import sys

def Get():
  """
  Gets the piped arguments, if they are present reopens sys.stdin back to tty.

  Returns
  -------
  Piped text (if wasnt any, then "").
  """
  # Get piped input
  pipe = ""
  if not sys.stdin.isatty(): # Check whether input was piped
    for i in sys.stdin:
      pipe += i

  # Reopen stdin, was pipe -> became tty
  if not sys.stdin.isatty():
    sys.stdin.close()
    try:
      sys.stdin = open("/dev/tty", 'r') # Open linux/mac
    except:
      try:
        sys.stdin = open("CONIN$", 'r') # Open windows
      except:
        pass # Dont do anything if a tty wasnt found, maybe user uses vim

  return pipe

