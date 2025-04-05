import argparse
from pathlib import Path
import sys

# Create arg parser
__parser = argparse.ArgumentParser()

# Add all necessary args
__parser.add_argument("-u", "--url", help="The LLM server url.", type=str, default="http://localhost:8080")
__parser.add_argument("-m", "--model", help="The name of the model that is going to be used from the server.", type=str, default="default")

__parser.add_argument("-a", "--api", help="The API for a model, only specify if not running locally.", type=str, default=None)

__parser.add_argument("-w", "--path", help="The path or paths for LLM to read from. Can either be a file or a directory, if directory additionally -r can be used.",
                     type=Path, nargs="*", default=[])
__parser.add_argument("-r", "--recursive", help="Look into directories recursively.", action="store_true")
__parser.add_argument("-e", "--exclude", help="Exclude specific directories or files from showing them to LLM.", nargs='*', default=[], type=Path)

__parser.add_argument("-t", "--temperature", type=float, 
                    help="The temperature of LLM's response. If not specified then 0.7 is used. The closer to 0 the more straight-forward the output is. The limit is 1.",
                    default=0.7)

__parser.add_argument("-l", "--history-length", type=int, help="The length of history of conversation saved, defaults to 3.", default=3)
__parser.add_argument("-c", "--history-clear", help="Clears the history and records the new conversation.", action="store_true")
__parser.add_argument("-n", "--no-history", help="Disables history just for 1 prompt, and turns it back on like nothing happened after.", action="store_true")

__parser.add_argument("-s", "--shell", help="Executes commands asked by a prompt in shell.", action="store_true")

__parser.add_argument("-p", "--prompt", help="User's prompt", nargs='*')

__parser.add_argument("-d", "--cache-location", help="Overrides the default cache directory. The default location is user's cache directory. Unrecommended to change.",
                      default=None, type=Path)

__parser.add_argument("-f", "--limit-history", help="If set then file contents given to LLM is not saved to history, only user prompt and answer are saved. Recommended to use with small context windows.", action="store_true")

__parser.add_argument("-o", "--code", help="If set outputs only in code format.", action="store_true")

__args = __parser.parse_args()

# Get piped input
__args.pipe = ""
if not sys.stdin.isatty(): # Check whether input was piped
  for i in sys.stdin:
    __args.pipe += i

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

def GetArgs():
  """This function returns an object with attributes of parsed arguments."""
  return __args
