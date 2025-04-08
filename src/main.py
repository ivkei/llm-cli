import argparser
import paths
import os
import platform
import history
import llmserver
import llmsystemprompts
import commandshandler
import datetime
import sys
from pathlib import Path

# Appname for config and history location
appname = ".llm-cli" # . for directory

# Get parsed args
args = argparser.GetArgs()

# Get client's prompt
prompt = " ".join(args.prompt or '') # join is used because of spaces in prompt

# Restore or create a default config if needed
if args.default_config:
  paths.CreateDefaultConfig(appname)

  if len(prompt) == 0 and not args.history_clear:
    exit(0) # Exit if empty prompt, dont exit if clear history requested, it will exit there

# If config doesnt exist
elif not paths.GetConfigFilePath(appname).exists():
  paths.CreateDefaultConfig(appname)

# Import config file if possible
config = None
configPath = paths.GetOSAppDir(appname)/"config.py"
if configPath.exists():
  sys.path.append(f"{configPath.parent}")
  import config
  # Dont mind the errors (if they appear), I tested and everything works great

# Set the config values with parsed arguments, after creating the config itself (or restoring)
argparser.SetConfigValues(appname)
  
# Init the server
llmserver.Init(config.url, config.api)

# Add the system prompt
requirements = llmsystemprompts.GetDefault()

if args.shell:
  requirements += llmsystemprompts.GetShell()

if args.code:
  requirements += llmsystemprompts.GetCode()

llmserver.AddSystemPropmt(requirements)

# Set history file location
history.historyFilePath = Path(config.history_directory)

# Set history length
historyLength = config.history_length if config.history_length >= 0 else 0 # Handle possible negative input
history.historyLimit = historyLength * 2 # * 2 because prompt and output are saved

# If clear history flag is on
if args.history_clear:
  history.ClearHistory()
  if len(prompt) == 0:
    exit(0)

# Pull out previous responses from the history and feed them along with current ones, if history is enabled
elif config.toggle_history:
  historyEntries = history.Deserialize()
  i = 0
  while i < len(historyEntries):
    llmserver.AddUserPropmt(historyEntries[i])
    i += 1
    llmserver.AddAssistantPropmt(historyEntries[i])
    i += 1
  
# Create full prompt
fullPrompt = f"""\
Contents: {args.pipe}\n\
{paths.GetPathsContents(args.path, args.exclude, args.recursive)}\n\
My Prompt: {prompt}
"""

# Inform LLM about current contents, user prompt, CWD, system and release.
llmserver.AddUserPropmt(f"""\
{fullPrompt}\n\
CWD: {os.getcwd()}\n\
System: {platform.system()}\n\
Release: {platform.release()}\n\
Current time: {datetime.datetime.now()}
""")
# Escape characters are added for proper formatting

def main():
  # Generate and print stream output
  temperature = config.temperature if config.temperature >= 0 else 0
  output = llmserver.PrintRespond(model=config.model, temperature=temperature, isStreaming=True, doIgnoreTripleBacktick=args.code and not args.shell)

  # Save the response and prompt to history, only if history is enabled
  if config.toggle_history: # If saving to history
    if config.toggle_limit_history: # If limit history, dont save contents
      history.Serialize(prompt) # Serialize only the prompt
    else:
      history.Serialize(fullPrompt) # Else serialize the contents also

    history.Serialize(output)

  # If commands were asked to execute
  if args.shell:
    commands = []
    parsingCommands = False
    for line in output.splitlines(): # Parse commands into a list
      # Only parse commands within ```sh ``` syntax, and from the last ```sh ``` box
      if line.startswith("```"):
        if not parsingCommands: commands.clear() # Clear so only last box commands are included
        parsingCommands = not parsingCommands
        continue

      # Only parse when necessary
      if parsingCommands:
        commands.append(line)

    # If commands are empty, no commands were found
    if len(commands) == 0:
      exit(0)

    # Clear prompt about format and give the LLM its output
    llmserver.ClearSystemPrompts()
    llmserver.AddSystemPropmt(llmsystemprompts.GetDefault())
    llmserver.AddAssistantPropmt(output)
      
    # Ask and execute the commands
    commandshandler.PromptUserAndExecute(commands, model=config.model, temperature=temperature)

# Call main
if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    print(f"\nKeyboardInterrupt")


# TODO:
# The changes to config dont display in file
# Add message to README how the new system works (set the config)
# Refactor all arguments and config stuff
  # appname should be all files global (or dont even exist)
  # names of configs and histories
  # move away the config and history functionalities away from paths module (may be even remake the structure)
