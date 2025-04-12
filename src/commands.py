"""
This module is made to handle -s flag, that asks to execute commands in shell.
"""
import server
import sysprompts
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
  for command in commands:
    # Get process and its stdout and stdin
    process = subprocess.Popen(command, shell=True, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr, text=True)
    process.wait()

def ReplacePlaceholders(commands : list):
  """
  Replaces all placeholders in commands, placeholder can be found in sysprompts, with values given by user.
  
  Parameters
  ----------
  @commands@ is list of commands to replace placeholders in
  """
  placeHolderIdx = 1
  for i in range(len(commands)):
    while True:
      # Loop condition here, because otherwise code repetition would occur
      phIndex = commands[i].find(sysprompts.GetPlaceholder())
      if phIndex == -1:
        break

      # Get value to replace placeholder with
      valueToReplaceWith = input(f"Enter value for {sysprompts.GetPlaceholder()}{placeHolderIdx}: ")

      # Replace the placeholder and its index with a value
      commands[i] = commands[i][:phIndex] + valueToReplaceWith + commands[i][
        phIndex + len(sysprompts.GetPlaceholder()) + len(str(placeHolderIdx)):
      ] 
      
      # Increment placeholder index
      placeHolderIdx += 1

def PromptUserAndExecute(commands : list, model : str, temperature : float, newLine : bool):
  """
  Asks a user whether to execute, abort or describe. To describe uses server.


  Parameters
  ----------
  @commands@ is list of commands to execute.
  @model@ is the name of previously initialized server model to access.
  @temp@ is the temperature of the model's output when commands are described.
  @newLine@ determines whether prompt for the user, about whether to execute or not, is on the new line.
  """
  # Prompt user and ask to execute
  action = ''
  while action != 'e': # As long as user doesnt execute commands
    action = input(f"{'\n' if newLine else ''}[E]xecute, [D]escribe, [A]bort: ")
    if action.lower() == 'a': exit(0) # Exit on Abort
    if action.lower() == 'd': # Describe
      # Add prompts and print response
      server.AddUserPropmt("Describe")
      server.PrintRespond(model=model, temperature=temperature, isStreaming=True)
      continue

    # If didnt abort, then replace placeholders with actual input
    ReplacePlaceholders(commands) 
      
    Execute(commands)

def ParseCommandsPromptUserExecute(output, model, temperature, parseOnlyInBackticks=False, newLine=True):
  """
  This function parses commands in @output@ argument and then prompts the user whether to execute them or not.
  If user chooses so, the commands are executed.
  Also option to describe exists for the user.

  Parameters
  ----------
  @output@ is the previous output of LLM, commands are found in it.
  @model@ is the model to use from already Init server.
  @temperature@ is the temperature of the response.
  @parseOnlyInBackticks@ is responsible for parsing only commands located in ```. If False then everyline is parsed as a command.
  @newLine@ determines whether prompt for the user, about whether to execute or not, is on the new line.
  """
  commands = []
  parsingCommands = False
  for line in output.splitlines(): # Parse commands into a list
    # Only parse commands within ```sh ``` syntax
    if line.startswith("```"):
      # if not parsingCommands: commands.clear() # Clear so only last box commands are included
      parsingCommands = not parsingCommands
      continue

    # Only parse when necessary
    if parsingCommands or not parseOnlyInBackticks:
      commands.append(line)

  # If commands are empty, no commands were found
  if len(commands) == 0:
    exit(0)

  # Make the LLM know about its previous prompt (and also clear the system propmt that told to output in specific format)
  # With this approach theres not history limit, but its not really needed here to keep the history, the context window should server in advance
  server.ClearSystemPrompts()
  server.AddSystemPropmt(sysprompts.GetDefault())
  server.AddAssistantPropmt(output)
    
  # Ask and execute the commands
  PromptUserAndExecute(commands, model=model, temperature=temperature, newLine=newLine)
