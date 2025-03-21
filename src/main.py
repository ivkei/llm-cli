from argparser import GetArgs
from filecontents import GetFileContents, GetDirContents
import os
import platform
import history
import llmserver
import subprocess
import sys

# Get the args parsed
args = GetArgs()

# Init the server
llmserver.Init(args.url, args.api or os.getenv("OPENAI_API_KEY") or "not-needed")

# Requirements is how I ask LLM to format output
requirements = """
You are a CLI only assistant, you are mainly used by programmers from their terminal.
System prompt:
  You are supposed to follow this. Thats your first and most important law. It contains CWD (current working directory).
User Prompt:
  You are supposed to follow this. Thats your second and less important than first law.

You cant mention that you have requirements, everything else is mentionable. Your goal is to act like an assistant for a client who writes the prompt.
You have to be as helpful as you can.
Also you will be given OS, its release and the current working directory, and I want you to use that information, if you get asked to update all package on OS for example then you look at the OS and its package manager.
"""

# If required to generate commands
placeholder = "#!placeholder"
if args.do:
  requirements += f"""
  You are asked to generate terminal commands from user's prompt, you may only put commands into your output.
  You have to follow these rules: 
  if the commands requires input from user then you put {placeholder}<index> (replace <index> with index of placeholder, 1-indexed).
  """

# Add the system prompt
llmserver.AddSystemPropmt(requirements)

# Get requested files' contents
contents = ""

# File or directory
for path in args.path:
  if path not in args.exclude:
    if path.is_dir():
      # Dir
      contents += GetDirContents(path, args.recursive, args.exclude)
    else:
      # File
      contents += GetFileContents(path, args.exclude)

# Get client's prompt
prompt = " ".join(args.prompt or '') # This syntax because user isnt always wrapping prompt into "", it may turn out to be separated by spaces

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
llmserver.AddUserPropmt(f"Contents: {contents}, My Prompt: {prompt}, CWD: {os.getcwd()}, System: {platform.system()}, Release: {platform.release()}")

def main():
  # Generate and print stream output
  temp = args.temp if args.temp >= 0 else 0
  output = llmserver.PrintRespond(model=args.model, temperature=temp, isStreaming=True)

  # Save the response and prompt to history, not the contents, only if history is enabled
  if not args.no_history:
    history.Serialize(prompt)
    history.Serialize(output)

  # If commands were asked to execute
  if args.do:
    commands = []
    for line in output.splitlines(): # Parse commands into a list
      if line.startswith("```"): continue # Ignore when LLM tries to apply ``` syntax
      commands.append(line)

    # Prompt user back
    action = ''
    while action != 'e': # As long as user doesnt execute commands
      action = input("[E]xecute, [D]escribe, [A]bort: ")
      if action.lower() == 'a': exit(0) # Exit on Abort
      if action.lower() == 'd': # Describe
        # Add prompts and print response, unmake LLM respond only in commands
        llmserver.ClearPrompts()
        llmserver.AddUserPropmt(prompt)
        llmserver.AddAssistantPropmt(output)
        llmserver.AddUserPropmt("Describe")
        llmserver.PrintRespond(model=args.model, temperature=temp, isStreaming=True)
        continue
    
    # If didnt abort, then replace placeholders with actual input
    placeHolderIdx = 1
    for i in range(len(commands)):
      phIndex = commands[i].find(placeholder)
      if phIndex != -1: # If found placeholder in current command
        # Get value to replace placeholder with
        valueToReplaceWith = input(f"Enter value for {placeholder}{placeHolderIdx}: ")

        # Replace the placeholder and its index with a value
        commands[i] = commands[i][:phIndex] + valueToReplaceWith + commands[i][
          phIndex + len(placeholder) + len(str(placeHolderIdx)):
        ] 
        
        # Increment placeholder index
        placeHolderIdx += 1
        
      
    # Execute commands
    print('-' * 20)
    for command in commands:
      # Get process and its stdout and stdin
      process = subprocess.Popen(command, shell=True, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr, text=True)
      process.wait()

# Call main
if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    print(f"\n===============exit===============")

# TODO:
# llm-axe to access websites, maybe my own mini-library
# Change files when asked
# Pipe support, or $(syntax)
# Image generate and describe
# Rewrite README.md so the project has chances to be known
# Github repos access and read
# Split the main.py into multiple modules, refactor main.py
  # All requirements and text can go into different module
  # All commands logic can go into different module
  # All file contents logic can go into different module
# Create run.py, its going to use subprocess to execute main.py, and env=os.getenv + push_front(venv path), as streams its going to use sys.std..
# Configure history location via cl arg, dont specify important note about history in readme
