"""
This module is responsible for config.
It can fetch.
It can push.
Before always set the path attribute of the module to point at the correct config.py file
This module's name is aconfig because I want the actual config file to keep its name (config.py), and if they both are configs, then there may be trouble importing.
"""
from pathlib import Path
import sys
from paths import CreatePath

path = None # Maybe errors because path may be None (if programmer doesnt specify the path

def Exists():
  return path.exists()

def CreateDefault():
  """
  Creates a default config with default values in them.
  """

  if not Exists():
    CreatePath(path)

  with open(path, 'w') as configFile:
    # \ at the ends for correct format
    configFile.write(f"""\
url = "http://localhost:8080" # Url of the server with LLM
model = "default" # Model for the server
api = "not-needed" # API, if using openai's LLMs
temperature = 0.7 # Temperatures above 1 will be considered 1, below 0 - 0
history_length = 3
toggle_limit_history = False
toggle_history = True
md_shell = True\
""")

def __GetConfig():
  """
  This function returns the config as an object with its attributes.
  """
  sys.path.append(f"{path.parent}")
  import config # Ignore the error if occurs
  return config

def GetAndSetMissingArgs(args):
  """
  Assumes the config file was already created.
  Assumes the path attribute of the module was set properly.
  Gets and set missing (None) arguments recieved by cli module.
  And also sets the right values for the toggle_history and toggle_limit_history config values.
  This function has to get called before SetFileValues.

  Parameters
  ----------
  @args@ is the object that has missing arguments returned by cli module.
  """
  config = __GetConfig()

  with open(path, 'w') as configFile:
    if not args.url:
      args.url = config.url

    if not args.api:
      args.api = config.api

    if not args.model:
      args.model = config.model

    if not args.temperature:
      args.temperature = config.temperature

    if not args.history_length:
      args.history_length = config.history_length

    if args.toggle_limit_history:
      args.toggle_limit_history = not config.toggle_limit_history
    else:
      args.toggle_limit_history = config.toggle_limit_history

    if args.toggle_history:
      args.toggle_history = not config.toggle_history
    else:
      args.toggle_history = config.toggle_history

    if args.md_shell:
      args.md_shell = not config.md_shell
    else:
      args.md_shell = config.md_shell

def SetFileValues(args):
  """
  Sets the values from args in a config file.
  This function assumes the config file was already created.
  This function assumes that GetAndSetMissingArguments was already called.
  This function needs the path attribute of the module to be set properly.

  Parameters
  ----------
  @args@ is the object that already has all proper values that going to be written to config.
  """
  with open(path, 'w') as configFile:
    configFile.write(f"url = \"{args.url}\"\n")

    configFile.write(f"api = \"{args.api}\"\n")

    configFile.write(f"model = \"{args.model}\"\n")

    configFile.write(f"temperature = {args.temperature}\n")

    configFile.write(f"history_length = {args.history_length}\n")

    configFile.write(f"toggle_limit_history = {args.toggle_limit_history}\n")

    configFile.write(f"toggle_history = {args.toggle_history}\n")

    configFile.write(f"md_shell = {args.md_shell}\n")
