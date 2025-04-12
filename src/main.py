"""
This module is the main execution of the program, its not to be exported.
It dispatches the execution to smaller modules.
"""
import os
import platform
import datetime

import cli
import aconfig
import pipe
import history
import sysprompts
import server
import commands
import files
import paths

def main() -> int:
  # Set the appname and whether the directory with it is hidden
  appname = "llm-cli"
  hidden = True
  paths.appname = appname
  paths.hidden = hidden

  args = cli.Parse()
  
  aconfig.path = paths.GetConfigFilePath() 
  if args.default_config or not aconfig.Exists(): 
    aconfig.CreateDefault()
  aconfig.GetAndSetMissingArgs(args)
  aconfig.SetFileValues(args)
  
  # Handle --show flag
  if len(args.show) > 0:
    for i in args.show:
      print(f"{i} is {args.__dict__[i]}")
  
  prompt = " ".join(args.prompt) # join because prompt may be separated by spaces (if client didnt use "")

  history.path = paths.GetHistoryFilePath()

  if args.clear_history:
    history.Clear()

  if len(prompt) == 0:
    return 0

  pipeContents = pipe.Get()

  filesContents = files.Parse(args.path, args.exclude, args.recursive)

  sysprompt = sysprompts.GetDefault()
  if args.shell:
    sysprompt += sysprompts.GetShell()
  if args.code:
    sysprompt += sysprompts.GetCode()

  server.Init(url=args.url, api=args.api)
  server.AddSystemPropmt(sysprompt)

  # Set the history length
  historyLength = args.history_length if args.history_length >= 0 else 0 # Handle negative
  history.length = historyLength * 2 # * 2 because the prompt and answer are saved

  # Get history
  if args.toggle_history and not args.clear_history:
    historyEntries = history.Deserialize()
    i = 0
    while i < len(historyEntries):
      server.AddUserPropmt(historyEntries[i])
      i += 1
      server.AddAssistantPropmt(historyEntries[i])
      i += 1

  fullPrompt = ""

  if len(pipeContents) > 0:
    fullPrompt += f"Piped input: {pipeContents}\n"

  if len(filesContents) > 0:
    fullPrompt += f"{filesContents}\n"
    fullPrompt += '\n'

  fullPrompt += prompt # No check for length because the program already checked for it (and exited if its)

  server.AddUserPropmt(f"""\
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
                               doIgnoreTripleBacktick=args.code or args.md_shell)

  # Serialize history
  if args.toggle_history: # If saving to history
    if args.toggle_limit_history: # If limit history, dont save contents
      history.Serialize(prompt) # Serialize only the prompt
    else:
      history.Serialize(fullPrompt) # Else serialize the contents also

    history.Serialize(output)

  if args.shell:
    commands.ParseCommandsPromptUserExecute(output,
                                            model=args.model,
                                            temperature=temperature,
                                            parseOnlyInBackticks=not args.md_shell,
                                            newLine=not args.md_shell)

  return 0

# Call main
try:
  exit(main())
except KeyboardInterrupt:
  print("KeyboardInterrupt")
  exit(0)

# TODO:
