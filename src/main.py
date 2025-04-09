import options as optionsModule
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
appname = "llm-cli"
hiddenAppDir = True

# Get parsed args
options = optionsModule.ParseOptions(appname=appname, hidden=hiddenAppDir)

# If clear history flag is on
if options.history_clear:
  history.ClearHistory()

# Restore or create a default config if needed
if options.default_config:
  optionsModule.CreateDefaultConfig(appname=appname, hidden=hiddenAppDir)

# Get client's prompt
prompt = " ".join(options.prompt or '') # join is used because of spaces in prompt

# If prompt is empty and theres a reason to exit, then do it
if len(prompt) == 0 and (len(options.path) == 0 and len(options.pipe) == 0):
  exit(0) # Exit if empty prompt, dont exit if clear history requested, it will exit there

# If config doesnt exist
if not paths.GetConfigFilePath(appname, hidden=hiddenAppDir).exists():
  optionsModule.CreateDefaultConfig(appname, hidden=hiddenAppDir)

# Init the server
llmserver.Init(options.url, options.api)

# Add the system prompt
requirements = llmsystemprompts.GetDefault()

if options.shell:
  requirements += llmsystemprompts.GetShell()

if options.code:
  requirements += llmsystemprompts.GetCode()

llmserver.AddSystemPropmt(requirements)

# Set history file location
history.historyFilePath = Path(options.history_directory)

# Set history length
historyLength = options.history_length if options.history_length >= 0 else 0 # Handle possible negative input
history.historyLimit = historyLength * 2 # * 2 because prompt and output are saved

# Pull out previous responses from the history and feed them along with current ones, if history is enabled
if options.toggle_history and not options.history_clear:
  historyEntries = history.Deserialize()
  i = 0
  while i < len(historyEntries):
    llmserver.AddUserPropmt(historyEntries[i])
    i += 1
    llmserver.AddAssistantPropmt(historyEntries[i])
    i += 1
  
# Create full prompt
fullPrompt = f"""\
Contents: {options.pipe}\n\
{paths.GetPathsContents(options.path, options.exclude, options.recursive)}\n\
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
  temperature = options.temperature if options.temperature >= 0 else 0
  output = llmserver.PrintRespond(model=options.model, temperature=temperature, isStreaming=True, doIgnoreTripleBacktick=options.code and not options.shell)

  # Save the response and prompt to history, only if history is enabled
  if options.toggle_history: # If saving to history
    if options.toggle_limit_history: # If limit history, dont save contents
      history.Serialize(prompt) # Serialize only the prompt
    else:
      history.Serialize(fullPrompt) # Else serialize the contents also

    history.Serialize(output)

  # If commands were asked to execute
  if options.shell:
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
    commandshandler.PromptUserAndExecute(commands, model=options.model, temperature=temperature)

# Call main
if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    print(f"\nKeyboardInterrupt")


# TODO:
# Add message to README how the new system works (set the config)
# If prompt is empty just exit
