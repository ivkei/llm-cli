"""
This module is responsible for config.
It can fetch.
It can push.
Before always set the path attribute of the module to point at the correct config.py file
This module's name is aconfig because I want the actual config file to keep its name (config.py), and if they both are configs, then there may be trouble importing.
"""
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
    "toggle_md_shell": False,
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
    for key, value in defaults.items():
      if type(value) is str:
        configFile.write(f"{key} = '{value}'\n")
      else:
        configFile.write(f"{key} = {value}\n")

def __GetConfig():
  """
  This function returns the config as an object with its attributes.
  """
  sys.path.append(f"{path.parent}")
  import config # Ignore the error if occurs
  return config

def MergeWith(args):
  """
  Assumes the config file was already created.
  Assumes the path attribute of the module was set properly.
  Merges missing (None) arguments recieved by cli module with config values.
  And also sets the right values for the toggle_history and toggle_limit_history config values.
  This function has to get called before WriteFileValues.
  This function only gets the values, not sets, if a value is missing in config, then it will be set in WriteFileValues.
  If value is missing in the config, then the value will remain None. As in cli module when not set.

  Parameters
  ----------
  @args@ is the object that has missing arguments returned by cli module.
  """
  config = __GetConfig()
  defaults = GetDefaults()

  def GetConfigValue(attr : str): # This function exists because you cant just use "or None" on module if attribute doesnt exist
    try:
      return getattr(config, attr)
    except:
      return None # Return None if didnt find a value in config for WriteFileValues to handle that

  def MergeValue(flag : str):
    if getattr(args, flag) is None:
      setattr(args, flag, GetConfigValue(flag))

  def MergeBool(flag : str):
    configFlag = GetConfigValue(flag)
    flagValue = getattr(args, flag)

    if flagValue:
      if configFlag is not None:
        setattr(args, flag, not configFlag)
      else:
        setattr(args, flag, None) # The config is missing the flag, cant set it to opposite of config's
    else: # False
      if configFlag is not None:
        setattr(args, flag, configFlag)
      else:
        setattr(args, flag, None) # The flag is not set and also is not in config

  for key, value in defaults.items(): # Defaults are used here just because they have key of every config param, and values that have their types
    if type(value) is bool: # Defaults actually arent set here
      MergeBool(key)
    else:
      MergeValue(key)

def WriteFileValues(args):
  """
  Sets the values from args in a config file.
  This function assumes the config file was already created.
  This function assumes that MergeWith was already called.
  This function needs the path attribute of the module to be set properly.

  Parameters
  ----------
  @args@ is the object that already has all proper values that going to be written to config.
  """
  defaults = GetDefaults()

  with open(path, 'w') as configFile:

    def WriteOrDefault(flag : str, isValueStr : bool = False, doJoinFlagValuesInString : bool = False):
      flagValue = getattr(args, flag)

      if doJoinFlagValuesInString: # No check for none, because if doJoinFlagValuesInString is True, then we know that flag value is a list and not None
        configFile.write(f"{flag} = {'"' if isValueStr else ''}{" ".join(flagValue)}{'"' if isValueStr else ''}\n")

      elif flagValue is not None: # Write value to config
        configFile.write(f"{flag} = {'"' if isValueStr else ''}{flagValue}{'"' if isValueStr else ''}\n")

      else: # Create one because its not in config
        doCreate = input(f"Missing a config value for {flag}. Create default? [Y]es, [N]o: ") # Prompt the user about a missing value
        if doCreate.lower() == 'y':
          configFile.write(f"{flag} = {'"' if isValueStr else ''}{defaults[flag]}{'"' if isValueStr else ''}\n")
          setattr(args, flag, defaults[flag])

    # WriteOrDefault("url", isValueStr=True)
    # WriteOrDefault("api", isValueStr=True)
    # WriteOrDefault("model", isValueStr=True)
    # WriteOrDefault("temperature")
    # WriteOrDefault("history_length")
    # WriteOrDefault("toggle_limit_history")
    # WriteOrDefault("toggle_history")
    # WriteOrDefault("toggle_md_shell")
    # WriteOrDefault("sys_prompt", isValueStr=True, doJoinFlagValuesInString=type(args.sys_prompt) is list) # Join because of lack of "" when input via cli arg

    for key, value in defaults.items(): # Default used because it contains all keys (flags from config), and values (types for config)
      WriteOrDefault(key, isValueStr=type(value) is str, doJoinFlagValuesInString=type(getattr(args, key)) is list)

def MergeConfigWith(args):
  """
  This function is indented for outside use.
  It exists because for user thats irrational to call GetAndSetMissingArgs and WriteFileValues separately because they are too coupled.
  This function just calls them 2.
  """
  MergeWith(args)
  WriteFileValues(args)
