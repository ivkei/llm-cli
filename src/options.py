import paths
import argparse
from pathlib import Path
import sys
import paths

def GetConfigVariableNames():
  """
  Returns a dictionary with keys as variables, and values as their variable names
  """
  return {
    "url": "url",
    "model": "model",
    "api": "api",
    "temperature": "temperature",
    "history_length": "history_length",
    "app_directory": "app_directory",
    "toggle_limit_history": "toggle_limit_history",
    "toggle_history": "toggle_history"
  }

def CreateDefaultConfig(appname, hidden=False):
  """
  Creates a default config with default values in them.

  Parameters
  ----------
  @appname@ is a name of the app for which default config is generated. Here if I decide to change name of the application.
  @hidden@ is whether the appname's directory has . infront.
  """

  configPath = paths.GetConfigFilePath(appname=appname, hidden=hidden)

  if not configPath.exists():
    paths.CreatePath(configPath)

  variableNames = GetConfigVariableNames()

  with open(configPath, 'w') as config:
    # \ at the ends for correct format
    config.write(f"""\
{variableNames["url"]} = "http://localhost:8080" # Url of the server with LLM
{variableNames["model"]} = "default" # Model for the server
{variableNames["api"]} = "not-needed" # API, if using openai's LLMs
{variableNames["temperature"]} = 0.7 # Temperatures above 1 will be considered 1, below 0 - 0
{variableNames["history_length"]} = 3
{variableNames["app_directory"]} = "{paths.GetHistoryFilePath(appname=appname, hidden=hidden)}"
{variableNames["toggle_limit_history"]} = False
{variableNames["toggle_history"]} = True\
""")

def GetConfig(appname, hidden=False):
  """
  Returns the config module.
  Assumes the config was already created.
  """
  configPath = paths.GetConfigFilePath(appname=appname, hidden=hidden)
  sys.path.append(f"{configPath.parent}")
  import config # Ignore the error if occurs
  return config

def __GetPipedArguments(options):
  """
  Gets piped arguments and text and appends them to options.

  Parameters
  ----------
  @options@ are options to append attribute "pipe" to.
  """
# Get piped input
  options.pipe = ""
  if not sys.stdin.isatty(): # Check whether input was piped
    for i in sys.stdin:
      options.pipe += i

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

def __GetCLIArguments(config):
  """
  This function attaches parsed CLI arguments for the application to options

  Parameters
  ----------
  @config@ is the config module with values

  Returns
  -------
  @options@ a Namespace object with attributes of parsed arguments
  """
  # Create arg parser
  __parser = argparse.ArgumentParser()

  # VariableNames in config to set defaults
  variableNames = GetConfigVariableNames()

  # Flag disclaimer that the value set will last until new or config restored
  flagPermanentDisclaimer ="""
  When the flag is set the value will be kept until a new is set, or until default config is restored.
  """
  __parser.add_argument("-u", "--url", help=f"""
  The LLM server url.
  Defaults to localhost:8080.
  {flagPermanentDisclaimer}
  """, type=str, default=config.__dict__[variableNames["url"]])

  __parser.add_argument("-m", "--model", help=f"""
  The name of the model that is going to be used from the server.
  Defaults to default.
  {flagPermanentDisclaimer}
  """, type=str, default=config.__dict__[variableNames["model"]])

  __parser.add_argument("-a", "--api", help=f"""
  The API for a server.
  Defaults to not-needed.
  {flagPermanentDisclaimer}
  """, type=str, default=config.__dict__[variableNames["api"]])

  __parser.add_argument("-w", "--path", help="The path or paths for LLM to read from. Can either be a file or a directory, if directory additionally -r can be used.",
                       type=Path, nargs="*", default=[])
  __parser.add_argument("-r", "--recursive", help="Look into directories recursively.", action="store_true")
  __parser.add_argument("-e", "--exclude", help="Exclude specific directories or files from showing them to LLM.", nargs='*', default=[], type=Path)

  __parser.add_argument("-t", "--temperature", type=float, help=f"""
  The temperature of LLM's response.
  Defaults to 0.7.
  The closer to 0 the more straight-forward the output is. The limit is 1.
  {flagPermanentDisclaimer}
  """, default=config.__dict__[variableNames["temperature"]])

  __parser.add_argument("-l", "--history-length", type=int, help=f"""
  The length of history of conversation saved.
  Recommended to decrease with LLMs with small context window.
  Defaults to 3 previous questions and answers.
  {flagPermanentDisclaimer}
  """, default=config.__dict__[variableNames["history_length"]])

  __parser.add_argument("-c", "--history-clear", help="Clears the history, further if prompt is specified starts from an empty canvas.", action="store_true")

  __parser.add_argument("-n", "--toggle-history", help=f"""
  Disables/Enables history.
  Defaults to enabled.
  {flagPermanentDisclaimer}
  """, action="store_true")

  __parser.add_argument("-s", "--shell", help="Executes commands asked by a prompt in shell.", action="store_true")

  __parser.add_argument("-p", "--prompt", help="User's prompt", nargs='*', default='')

  __parser.add_argument("-d", "--app-directory", help=f"""
  Changes the directory that contains the history file.
  Unrecommended to change.
  Defaults to ~/.llm-cli/.
  {flagPermanentDisclaimer}
  """, default=config.__dict__[variableNames["app_directory"]], type=Path)

  __parser.add_argument("-f", "--toggle-limit-history", help=f"""
  When history is limited it means that contents of files specified is not saved along with the prompt.
  Recommended to disabled with LLMs with small context window.
  {flagPermanentDisclaimer}
  """, action="store_true")

  __parser.add_argument("-o", "--code", help="If set outputs only in code format.", action="store_true")

  __parser.add_argument("-b", "--default-config", help="Restores the default config.", action="store_true")

  options = __parser.parse_args()
  
  if options.toggle_history:
    options.toggle_history = not config.__dict__[variableNames["toggle_history"]]
  else:
    options.toggle_history = config.__dict__[variableNames["toggle_history"]]
  
  if options.toggle_limit_history:
    options.toggle_limit_history = not config.__dict__[f"{variableNames["toggle_limit_history"]}"]
  else:
    options.toggle_limit_history = config.__dict__[f"{variableNames["toggle_limit_history"]}"]

  return options

def __SetConfigValues(options, appname, hidden=False):
  """
  This function sets all the config values that were requested to be changed by CLI arguments set.
  It assumes that config was already created.

  Parameters
  ----------
  @appname@ is a name of the application for the directory with config.
  @hidden@ determines whether the application directory with config is hidden (. in front).
  @options@ are options that already have set flags for serialization to config. 
  """

  configPath = paths.GetConfigFilePath(appname=appname, hidden=hidden)

  variableNames = GetConfigVariableNames()

  with open(configPath, 'w') as configFile:
    # Save the url to config
    configFile.write(f"{variableNames["url"]} = \"{options.url}\"\n")

    # Save the api to config
    configFile.write(f"{variableNames["api"]} = \"{options.api}\"\n")

    # Save the model to config
    configFile.write(f"{variableNames["model"]} = \"{options.model}\"\n")

    # Save the temperature to config
    configFile.write(f"{variableNames["temperature"]} = {options.temperature}\n")

    # Save the history length to config
    configFile.write(f"{variableNames["history_length"]} = {options.history_length}\n")

    # Save limit history toggle to config
    configFile.write(f"{variableNames["toggle_limit_history"]} = {options.toggle_limit_history}\n")

    # Save toggle history to config
    configFile.write(f"{variableNames["toggle_history"]} = {options.toggle_history}\n")

    # Save history directory to config
    configFile.write(f"{variableNames["app_directory"]} = \"{options.app_directory}\"\n")

def ParseOptions(appname, hidden=False):
  """
  Parses arguments and config values, and returns them.
  Assumes that config already exists (can be created by CreateDefaultConfig function).

  Parameters
  ----------
  @appname@ is the name of the app for the config to find its directory.
  @hidden@ determines whether the directory that contains the config is hidden (. in front).

  Returns
  -------
  @options@ are options with all the parsed CLI arguments, config values and piped text.
  """
  config = GetConfig(appname=appname, hidden=hidden)
  options = __GetCLIArguments(config)
  __GetPipedArguments(options)
  __SetConfigValues(options=options, appname=appname, hidden=hidden)
  return options
