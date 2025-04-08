import argparse
from pathlib import Path
import sys
import paths

# Create arg parser
__parser = argparse.ArgumentParser()

# Add all necessary args, if default is None, then in the SetConfigValues the value to set in config is skipped,
# all actual default values of those with None are stored in the paths module (CreateDefaultConfig function)

# Flag disclaimer that the value set will last until new or config restored
flagPermanentDisclaimer ="""
When the flag is set the value will be kept until a new is set, or until default config is restored.
"""
__parser.add_argument("-u", "--url", help=f"""
The LLM server url.
Defaults to localhost:8080.
{flagPermanentDisclaimer}
""", type=str, default=None)

__parser.add_argument("-m", "--model", help=f"""
The name of the model that is going to be used from the server.
Defaults to default.
{flagPermanentDisclaimer}
""", type=str, default=None)

__parser.add_argument("-a", "--api", help=f"""
The API for a server.
Defaults to not-needed.
{flagPermanentDisclaimer}
""", type=str, default=None)

__parser.add_argument("-w", "--path", help="The path or paths for LLM to read from. Can either be a file or a directory, if directory additionally -r can be used.",
                     type=Path, nargs="*", default=[])
__parser.add_argument("-r", "--recursive", help="Look into directories recursively.", action="store_true")
__parser.add_argument("-e", "--exclude", help="Exclude specific directories or files from showing them to LLM.", nargs='*', default=[], type=Path)

__parser.add_argument("-t", "--temperature", type=float, help=f"""
The temperature of LLM's response.
Defaults to 0.7.
The closer to 0 the more straight-forward the output is. The limit is 1.
{flagPermanentDisclaimer}
""", default=None)

__parser.add_argument("-l", "--history-length", type=int, help=f"""
The length of history of conversation saved.
Recommended to decrease with LLMs with small context window.
Defaults to 3 previous questions and answers.
{flagPermanentDisclaimer}
""", default=None)

__parser.add_argument("-c", "--history-clear", help="Clears the history, further if prompt is specified starts from an empty canvas.", action="store_true")

__parser.add_argument("-n", "--toggle-history", help=f"""
Disables/Enables history.
Defaults to enabled.
{flagPermanentDisclaimer}
""", action="store_true")

__parser.add_argument("-s", "--shell", help="Executes commands asked by a prompt in shell.", action="store_true")

__parser.add_argument("-p", "--prompt", help="User's prompt", nargs='*', default='')

__parser.add_argument("-d", "--history-directory", help=f"""
Changes the directory that contains the history file.
Unrecommended to change.
Defaults to ~/.llm-cli/.
{flagPermanentDisclaimer}
""", default=None, type=Path)

__parser.add_argument("-f", "--toggle-limit-history", help=f"""
When history is limited it means that contents of files specified is not saved along with the prompt.
Recommended to disabled with LLMs with small context window.
{flagPermanentDisclaimer}
""", action="store_true")

__parser.add_argument("-o", "--code", help="If set outputs only in code format.", action="store_true")

__parser.add_argument("-b", "--default-config", help="Restores the default config.", action="store_true")

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

def SetConfigValues(appname):
  """
  This function sets all the config values that were requested to be changed by CLI arguments set.
  It assumes that config was already created.

  Parameters
  ----------
  @appname@ is a name of the application for the directory with config.
  """
  # Import config file
  config = None
  configPath = paths.GetConfigFilePath(appname)
  if configPath.exists():
    sys.path.append(f"{configPath.parent}")
    import config
    # Dont mind the errors (if they appear), I tested and everything works great

  # Sets
  if __args.url:
    config.url = __args.url

  if __args.api:
    config.api = __args.api

  if __args.model:
    config.model = __args.model

  if __args.temperature:
    config.temperature = __args.temperature

  if __args.history_length:
    config.history_length = __args.history_length

  if __args.toggle_limit_history:
    config.toggle_limit_history = not config.toggle_limit_history

  if __args.toggle_history:
    config.toggle_history = not config.toggle_history

  if __args.history_directory:
    config.history_directory = __args.history_directory
