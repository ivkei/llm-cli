from pathlib import Path
from os import name 
from functools import cache
from os import makedirs

def GetDirContents(path, recursive, excludes : list) -> str:
  """Parses a directory and concatenates all file contents into 1, with ParseFile's format, either recursively and with ability to exclude files or dirs.

  Parameters
  ----------
  @path@ is path to get contents from.
  @excludes@ are files or directories to not get contents from.
  @recursive@ determines whether to go deep into a directory on no.
  """
  contents = ""
  for path in path.iterdir():
    if path.is_dir():
      # Dir
      if recursive and path not in excludes:
        # Parse if needed
        contents += GetDirContents(path, recursive, excludes)
    else:
      # File
      contents += GetFileContents(path, excludes)
  return contents

def GetFileContents(path, excludes : list) -> str:
  """Parses a file and returns its contents in following format: \"Relative Path: {path}\\nContents:\n{file.contents}\"

  Parameters
  ----------
  @path@ is path to get contents from.
  @excludes@ are files to not get contents from.
  """
  if path in excludes: return ""
  with path.open('r', errors="ignore") as file:
    return f"""Relative Path: {path}\nContents:\n{file.read()}
    """

def GetPathsContents(paths : list, excludes : list, recursive):
  """Gets contents of either directories or files at paths with few options.
  
  Parameters
  ----------
  @paths@ are paths to get contents from.
  @excludes@ are files or directories to not get contents from.
  @recursive@ determines whether to go deep into a directory on no.
  """
  # Get requested files' contents
  contents = ""

  # File or directory
  for path in paths:
    if path not in excludes:
      if path.is_dir():
        # Dir
        contents += GetDirContents(path, recursive, excludes)
      else:
        # File
        contents += GetFileContents(path, excludes)

  return contents

@cache
def GetOSCacheDir(appname=None) -> Path:
  """
  Returns the cache directory for an application.
  On linux its ~/.cache/appname (if appname is specified).
  On windows its ~/AppData/Local/Temp/appname.

  Parameters
  ----------
  @appname@ is name of the app to return cache directory of,
  if not specified then the cache directory is returned.

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

  if appname:
    cacheDir /= f"{appname}/"

  return cacheDir

@cache
def GetOSConfigDir(appname=None) -> Path:
  """
  Returns the config directory for an application.
  On linux its ~/.config/appname (if appname is specified).
  On windows its ~/AppData/Local/appname.

  Parameters
  ----------
  @appname@ is name of the app to return cache directory of,
  if not specified then the cache directory is returned.

  Returns
  -------
  A directory for config, depends on the appname
  """
  
  user = Path.home()
  configDir = None

  if name == "nt": # Windows
    configDir = user/"AppData/Local/"

  else: # Linux and Mac
    configDir = user/".cache/"

  if appname:
    configDir /= f"{appname}/"

  return configDir

@cache
def GetOSAppDir(appname) -> Path:
  """
  Returns the application directory, its always ~/appname.

  Parameters
  ----------
  @appname@ is name of the app to return directory of,
  if not specified then the cache directory is returned.

  Returns
  -------
  An application directory, depends on the appname.
  """

  user = Path.home()
  return user/f"{appname}/"

def GetConfigFilePath(appname):
  """
  Returns a config file path for the application
  """
  return GetOSAppDir(appname)/"config.py"

def GetHistoryFilePath(appname):
  """
  Returns a config file path for the application
  """
  return GetOSAppDir(appname)/"history"

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

def CreateDefaultConfig(appname):
  """
  Creates a default config with default values in them.

  Parameters
  ----------
  @appname@ is a name of the app for which default config is generated. Here if I decide to change name of the application.
  """

  configPath = GetConfigFilePath(appname)

  if not configPath.exists():
    CreatePath(configPath)

  with open(configPath, 'w') as config:
    # \ at the ends for correct format
    config.write(f"""\
url = "http://localhost:8080"
model = "default"
api = "not-needed"
temperature = 0.7
history_length = 3
history_directory = "{GetHistoryFilePath(appname)}"
toggle_limit_history = False
toggle_history = True\
""")
