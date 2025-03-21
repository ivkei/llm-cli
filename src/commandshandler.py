import llmserver
import llmsystemprompts
import subprocess
import sys

def Execute(commands : list):
  """
  Executes given list of commands on sys.stdout, and uses sys.stdin and sys.stderr.

  Parameters
  ----------
  @commands@ is list of commands to execute.
  """
  # Execute commands
  print('-' * 20)
  for command in commands:
    # Get process and its stdout and stdin
    process = subprocess.Popen(command, shell=True, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr, text=True)
    process.wait()

def ReplacePlaceholders(commands : list):
  """
  Replaces all placeholders in commands, placeholder can be found in llmsystemprompts, with values given by user.
  
  Parameters
  ----------
  @commands@ is list of commands to replace placeholders in
  """
  placeHolderIdx = 1
  for i in range(len(commands)):
    phIndex = commands[i].find(llmsystemprompts.GetPlaceholder())
    if phIndex != -1: # If found placeholder in current command
      # Get value to replace placeholder with
      valueToReplaceWith = input(f"Enter value for {llmsystemprompts.GetPlaceholder()}{placeHolderIdx}: ")

      # Replace the placeholder and its index with a value
      commands[i] = commands[i][:phIndex] + valueToReplaceWith + commands[i][
        phIndex + len(llmsystemprompts.GetPlaceholder()) + len(str(placeHolderIdx)):
      ] 
      
      # Increment placeholder index
      placeHolderIdx += 1

def AskAndExecute(commands : list, model : str, temperature : float):
  """
  Asks a user whether to execute, abort or describe. To describe uses llmserver.


  Parameters
  ----------
  @commands@ is list of commands to execute.
  @model@ is the name of previously initialized llmserver model to access.
  @temp@ is the temperature of the model's output when commands are described.
  """
  # Prompt user and ask to execute
  action = ''
  while action != 'e': # As long as user doesnt execute commands
    action = input("[E]xecute, [D]escribe, [A]bort: ")
    if action.lower() == 'a': exit(0) # Exit on Abort
    if action.lower() == 'd': # Describe
      # Add prompts and print response, unmake LLM respond only in commands
      llmserver.AddUserPropmt("Describe")
      llmserver.PrintRespond(model=model, temperature=temperature, isStreaming=True)
      continue

    # If didnt abort, then replace placeholders with actual input
    ReplacePlaceholders(commands) 
      
    Execute(commands)
