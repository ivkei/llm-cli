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

def GetDefaults() -> dict:
  """
  Returns a dictionary with default values, needed for no code repetition,
  and if I wanted to change a default value, I didnt have to do that in 25 places.

  Returns
  -------
  @dict@ with default values and keys as their names.
  """
  return {
    "url": "http://localhost:8080",
    "model": "default",
    "api": "not-needed",
    "temperature": 0.7,
    "history_length": 3,
    "toggle_limit_history": False,
    "toggle_history": True,
    "toggle_md_shell": True,
    "sys_prompt": '',
  }

def CreateDefault():
  """
  Creates a default config with default values in them.
  """

  if not Exists():
    CreatePath(path)

  defaults = GetDefaults()

  with open(path, 'w') as configFile:
    # \ at the ends for correct format
    configFile.write(f"""\
url = {defaults["url"]} # URL of the server with LLM
model = {defaults["model"]} # Model, specify only for multi-model servers
api = {defaults["api"]} # API, if using openai's LLMs
temperature = {defaults["temperature"]} # Temperatures above 1 will be considered 1, below 0 - 0
history_length = {defaults["history_length"]}
toggle_limit_history = {defaults["toggle_limit_history"]}
toggle_history = {defaults["toggle_history"]}
toggle_md_shell = {defaults["toggle_md_shell"]}
sys_prompt = {defaults["sys_prompt"]}\
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
  This function has to get called before WriteFileValues.
  This function only gets the values, not sets, if a value is missing in config, then it will be set in WriteFileValues.
  If value is missing in the config, then the value will remain None. As in cli module when not set.

  Parameters
  ----------
  @args@ is the object that has missing arguments returned by cli module.
  """
  config = __GetConfig()

  def GetConfigValue(attr : str): # This function exists because you cant just use "or None" on module if attribute doesnt exist
    try:
      return getattr(config, attr)
    except:
      return None # Return None if didnt find a value in config for WriteFileValues to handle that


  if args.url is None:
    args.url = GetConfigValue("url")

  if args.api is None:
    args.api = GetConfigValue("api")

  if args.model is None:
    args.model = GetConfigValue("model")

  if args.temperature is None:
    args.temperature = GetConfigValue("temperature")

  if args.history_length is None:
    args.history_length = GetConfigValue("history_length")

  toggle_limit_historyConfig = GetConfigValue("toggle_limit_history")
  if args.toggle_limit_history:
    if toggle_limit_historyConfig: # Only get the value if config has it
      args.toggle_limit_history = not config.toggle_limit_history
    else:
      args.toggle_limit_history = None # Set to None for WriteConfigValues to create one
  else:
    if toggle_limit_historyConfig: # Only get the value if config has it
      args.toggle_limit_history = config.toggle_limit_history
    else:
      args.toggle_limit_history = None # Set to None for WriteConfigValues to create one

  toggle_historyConfig = GetConfigValue("toggle_history")
  if args.toggle_history:
    if toggle_historyConfig: # Only get the value if config has it
      args.toggle_history = not config.toggle_history
    else:
      args.toggle_history = None # Set to None for WriteConfigValues to create one
  else:
    if toggle_historyConfig: # Only get the value if config has it
      args.toggle_history = config.toggle_history
    else:
      args.toggle_history = None # Set to None for WriteConfigValues to create one

  toggle_md_shellConfig = GetConfigValue("toggle_md_shell")
  if args.toggle_md_shell:
    if toggle_md_shellConfig: # Only get the value if config has it
      args.toggle_md_shell = not config.toggle_md_shell
    else:
      args.toggle_md_shell = None # Set to None for WriteConfigValues to create one
  else:
    if toggle_md_shellConfig: # Only get the value if config has it
      args.toggle_md_shell = config.toggle_md_shell
    else:
      args.toggle_md_shell = None # Set to None for WriteConfigValues to create one

  if args.sys_prompt is None:
    args.sys_prompt = GetConfigValue("sys_prompt")

def WriteFileValues(args):
  """
  Sets the values from args in a config file.
  This function assumes the config file was already created.
  This function assumes that GetAndSetMissingArguments was already called.
  This function needs the path attribute of the module to be set properly.

  Parameters
  ----------
  @args@ is the object that already has all proper values that going to be written to config.
  """
  defaults = GetDefaults()

  with open(path, 'w') as configFile:
    if args.url is not None:
      configFile.write(f"url = \"{args.url}\"\n")
    else: # Create one because its not in config
      configFile.write(f"url = \"{defaults["url"]}\"\n")
      args.url = defaults["url"]

    if args.api is not None:
      configFile.write(f"api = \"{args.api}\"\n")
    else: # Create one because its not in config
      configFile.write(f"api = \"{defaults["api"]}\"\n")
      args.api = defaults["api"]

    if args.model is not None:
      configFile.write(f"model = \"{args.model}\"\n")
    else: # Create one because its not in config
      configFile.write(f"model = \"{defaults["model"]}\"\n")
      args.model = defaults["model"]

    if args.temperature is not None:
      configFile.write(f"temperature = {args.temperature}\n")
    else: # Create one because its not in config
      configFile.write(f"temperature = {defaults["temperature"]}\n")
      args.temperature = defaults["temperature"]

    if args.history_length is not None:
      configFile.write(f"history_length = {args.history_length}\n")
    else: # Create one because its not in config
      configFile.write(f"history_length = {defaults["history_length"]}\n")
      args.history_length = defaults["history_length"]

    if args.toggle_limit_history is not None:
      configFile.write(f"toggle_limit_history = {args.toggle_limit_history}\n")
    else: # Create one because its not in config
      configFile.write(f"toggle_limit_history = {defaults["toggle_limit_history"]}\n")
      args.toggle_limit_history = defaults["toggle_limit_history"]

    if args.toggle_history is not None:
      configFile.write(f"toggle_history = {args.toggle_history}\n")
    else: # Create one because its not in config
      configFile.write(f"toggle_history = {defaults["toggle_history"]}\n")
      args.toggle_history = defaults["toggle_history"]

    if args.toggle_md_shell is not None:
      configFile.write(f"toggle_md_shell = {args.toggle_md_shell}\n")
    else: # Create one because its not in config
      configFile.write(f"toggle_md_shell = {defaults["toggle_md_shell"]}\n")
      args.toggle_md_shell = defaults["toggle_md_shell"]

    if type(args.sys_prompt) is list: # This check because if input came from CLI, then words are in list, because of the spaces
      configFile.write(f"sys_prompt = \"{" ".join(args.sys_prompt)}\"\n") # Join because in cli divided by spaces -> list
    else: # Otherwise words are taken from config itself, and are in string
      if args.sys_prompt is not None:
        configFile.write(f"sys_prompt = \"{args.sys_prompt}\"\n")
      else: # Create one because its not in config
        configFile.write(f"sys_prompt = \"{defaults["sys_prompt"]}\"\n")
        args.sys_prompt = defaults["sys_prompt"]

def SetArgsFromConfigAndWriteFile(args):
  """
  This function is indented for outside use.
  It exists because for user thats irrational to call GetAndSetMissingArgs and WriteFileValues separately because they are too coupled.
  This function just calls them 2.
  """
  GetAndSetMissingArgs(args)
  WriteFileValues(args)
