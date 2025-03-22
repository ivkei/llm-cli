from argparser import GetArgs
import filecontents
import os
import platform
import history
import llmserver
import llmsystemprompts
import commandshandler

# Get the args parsed
args = GetArgs()

# Init the server
llmserver.Init(args.url, args.api or os.getenv("OPENAI_API_KEY") or "not-needed")

# Add the system prompt
requirements = llmsystemprompts.GetDefault()

if args.shell:
  requirements += llmsystemprompts.GetShell()

llmserver.AddSystemPropmt(requirements)

# Get client's prompt
prompt = " ".join(args.prompt or '') # This syntax because user isnt always wrapping prompt into "", it may turn out to be separated by spaces

# Set history file location
history.historyFilePath = args.history_location

# Set history length
historyLength = args.history_length * 2 if args.history_length >= 0 else 0 # Handle possible negative input
history.historyLimit = historyLength # * 2 because prompt and output are saved

# If clear history flag is on
if args.history_clear:
  history.ClearHistory()
elif not args.no_history: # Pull out previous responses from the history and feed them along with current ones, if history is enabled
  historyEntries = history.Deserialize()
  i = 0
  while i < len(historyEntries):
    llmserver.AddUserPropmt(historyEntries[i])
    i += 1
    llmserver.AddAssistantPropmt(historyEntries[i])
    i += 1
  
# Inform LLM about current contents, user prompt, CWD, system and release.
llmserver.AddUserPropmt(f"""
Contents: {args.pipe}\n{filecontents.GetPathsContents(args.path, args.exclude, args.recursive)},
My Prompt: {prompt},
CWD: {os.getcwd()},
System: {platform.system()},
Release: {platform.release()}
""")

def main():
  # Generate and print stream output
  temperature = args.temperature if args.temperature >= 0 else 0
  output = llmserver.PrintRespond(model=args.model, temperature=temperature, isStreaming=True)

  # Save the response and prompt to history, not the contents, only if history is enabled
  if not args.no_history:
    history.Serialize(prompt)
    history.Serialize(output)

  # If commands were asked to execute
  if args.shell:
    commands = []
    for line in output.splitlines(): # Parse commands into a list
      if line.startswith("```"): continue # Ignore when LLM tries to apply ``` syntax
      commands.append(line)

    # Clear prompt about format and give the LLM its output
    llmserver.ClearSystemPrompts()
    llmserver.AddSystemPropmt(llmsystemprompts.GetDefault())
    llmserver.AddAssistantPropmt(output)
      
    # Ask and execute the commands
    commandshandler.AskAndExecute(commands, model=args.model, temperature=temperature)

# Call main
if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    print(f"\n===============exit===============")

# TODO:
# llm-axe to access websites, maybe my own mini-library
# Change files when asked
# Mention pipe support in readme, also add that $() can be used
# Image generate and describe
# Rewrite README.md so the project has chances to be known, add TODO list there, after pipe support, history location
# Github repos access and read
# Create run.py, its going to use subprocess to execute main.py, and env=os.getenv + push_front(venv path), as streams its going to use sys.std..
  # Or just use pyinstaller
# Add flag to serialize full prompt with files and without
