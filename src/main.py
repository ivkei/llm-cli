"""
This module is the main execution of the program, its not to be exported.
It dispatches the execution to smaller layers.
"""
import os
import platform
import datetime

from layers import cli
from layers import config
from layers import pipe
from layers import history
from layers import sysprompts
from layers import server
from layers import commands
from layers import files
import paths

def main() -> int:
  # Set the appname and whether the directory with it is hidden
  appname = "llm-cli"
  hidden = True
  paths.appname = appname
  paths.hidden = hidden

  args = cli.Parse()
  
  config.path = paths.GetAppPath() 
  if args.default_config or not config.Exists(): 
    config.CreateDefaultConfig()
  config.GetAndSetMissingArgs(args)
  config.SetFileValues(args)
  
  prompt = "".join(args.prompt) # join because prompt may be separated by spaces (if client didnt use "")

  if args.clear_history:
    history.Clear()

  if len(prompt) == 0:
    return 0

  pipeContents = pipe.GetAndSet()

  filesContents = files.Parse(args.path, args.exclude, args.recursive)

  sysprompt = sysprompts.GetDefault()
  if args.shell:
    sysprompt += sysprompts.GetShell()
  if args.code:
    sysprompt += sysprompts.GetCode()

  server.Init(url=args.url, api=args.api)
  server.AddSystemPropmt(sysprompt)

  # Set necessary history fields
  history.path = paths.GetAppPath()
  historyLimit = args.history_limit if args.history_limit >= else 0 # Handle negative
  history.limit = historyLimit * 2 # * 2 because the prompt and answer are saved
  
  # Get history
  if args.toggle_history and not args.clear_history:
    historyEntries = history.Deserialize()
    i = 0
    while i < len(historyEntries):
      server.AddUserPropmt(historyEntries[i])
      i += 1
      server.AddAssistantPropmt(historyEntries[i])
      i += 1

  fullPrompt = f"""\
  Piped input:\n {pipeContents}\n\
  Files input:\n {filesContents}\n\
  Prompt: {prompt}\
  """

  llmserver.AddUserPropmt(f"""\
  {fullPrompt}\n\
  CWD: {os.getcwd()}\n\
  System: {platform.system()}\n\
  Release: {platform.release()}\n\
  Current time: {datetime.datetime.now()}\
  """)
  # Escape characters are added for proper formatting

  temperature = args.temperature if args.temperature >= 0 else 0 # Clamp
  temperature = temperature if temperature <= 1 else 1 # Clamp

  output = server.PrintRespond(model=args.model,
                               temperature=temperature,
                               isStreaming=True,
                               doIgnoreTripleBacktick=args.code and not args.shell)

  # Serialize history
  if args.toggle_history: # If saving to history
    if args.toggle_limit_history: # If limit history, dont save contents
      history.Serialize(prompt) # Serialize only the prompt
    else:
      history.Serialize(fullPrompt) # Else serialize the contents also

    history.Serialize(output)

  if args.shell:
    commands.ParsePromptUserExecute(output)

  return 0

# Call main
try:
  exit(main())
except KeyboardInterrupt:
  print("KeyboardInterrupt")
  exit(0)

# TODO:
# Delete the fully customizable from readme
# Delete the -d flag
# Rename ClearHistory to Clear
# Add datetime to credits
