"""
This module is responsible for parsing necessary arguments for the llm-cli application.
It has only one function Parse.
"""
import argparse
from pathlib import Path

def Parse():
  """
  This function parses necessary arguments for the llm-cli app, and returns them as an object.
  This function may leave some arguments as None, they have to be handled later (after fetching config).
  Also toggle_limit_history and toggle_history have to also be handled later (after fetching config).
  If config was imported before then it would be really hard to restore it with a flag.

  Returns
  -------
  An object with attributes of parsed arguments.
  """
  # Create arg parser
  __parser = argparse.ArgumentParser()

  # Flag disclaimer that the value set will last until new or config restored
  flagPermanentDisclaimer ="""
  When the flag is set the value will be kept until a new is set, or until default config is restored.
  """
  
  # For every argument with default of None, it will be handled later (loaded from config)

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

  __parser.add_argument("-c", "--clear-history", help="Clears the history, further if prompt is specified starts from an empty canvas.", action="store_true")

  __parser.add_argument("-n", "--toggle-history", help=f"""
  Disables/Enables history.
  Defaults to enabled.
  {flagPermanentDisclaimer}
  """, action="store_true")

  __parser.add_argument("-s", "--shell", help="Executes commands asked by a prompt in shell.", action="store_true")

  __parser.add_argument("-p", "--prompt", help="User's prompt", nargs='*', default='')

  __parser.add_argument("-f", "--toggle-limit-history", help=f"""
  When history is limited it means that contents of files specified is not saved along with the prompt.
  Recommended to disabled with LLMs with small context window.
  {flagPermanentDisclaimer}
  """, action="store_true")

  __parser.add_argument("-o", "--code", help="If set outputs only in code format.", action="store_true")

  __parser.add_argument("-b", "--default-config", help="Restores the default config.", action="store_true")

  options = __parser.parse_args()
  
  return options

