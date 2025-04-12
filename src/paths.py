"""
This module is responsible for working with paths.
It knows the paths for config and history.
It can create paths.
"""
from pathlib import Path
from os import name 
from functools import cache
from os import makedirs

appname = "llm-cli"
hidden = True

@cache
def GetOSCacheDir() -> Path:
  """
  Returns the cache directory for an application.
  On linux its ~/.cache/appname.
  On windows its ~/AppData/Local/Temp/appname.
  Depends on the appname and hidden variables set in the module.

  Returns
  -------
  A directory for cache, depends on the appname
  """
  
  user = Path.home()
  cacheDir = None

  if name == "nt": # Windows
    cacheDir = user/"AppData/Local/Temp/"

  else: # Linux and Mac
    cacheDir = user/".cache/"

  if hidden:
    cacheDir /= f".{appname}/"
  else:
    cacheDir /= f"{appname}/"


  return cacheDir

@cache
def GetOSConfigDir() -> Path:
  """
  Returns the config directory for an application.
  On linux its ~/.config/appname.
  On windows its ~/AppData/Local/appname.
  Depends on the appname and hidden variables that this module contains.

  Returns
  -------
  A directory for config, depends on the appname and hidden variables.
  """
  
  user = Path.home()
  configDir = None

  if name == "nt": # Windows
    configDir = user/"AppData/Local/"

  else: # Linux and Mac
    configDir = user/".cache/"

  if hidden:
    configDir /= f".{appname}/"
  else:
    configDir /= f"{appname}/"

  return configDir

@cache
def GetOSAppDir() -> Path:
  """
  Returns the application directory, its always ~/appname.
  Depends on the appname and hidden variables in this module.

  Returns
  -------
  An application directory, depends on the appname.
  """

  user = Path.home()

  appDir = None
  if hidden:
    appDir = user/f".{appname}/" 
  else:
    appDir = user/f"{appname}/" 

  return appDir

def GetConfigFilePath():
  """
  Returns a config file path for the application.
  Its location depends on the appname and hidden fields that this module has.
  """
  return GetOSAppDir()/"config.py"

def GetHistoryFilePath():
  """
  Returns a config file path for the application
  Its location depends on the appname and hidden variables set in the module.
  """
  return GetOSAppDir()/"history"

def CreatePath(path : Path):
  """
  Simulates behavior of mkdir -p, and also touches if file at the end of the path.

  Parameters
  ----------
  @path@ is a path to create.
  """

  makedirs(name=path.parent, exist_ok=True)

  if path.is_dir():
    path.mkdir(exist_ok=True)
  else: # File
    path.touch()
