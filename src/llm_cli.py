import cl_parser
import path_parser
from openai import OpenAI
import os
import history
from enum import Enum

args = cl_parser.GetArgs()

# Create LLM server access instance
llm = OpenAI(base_url=args.url, api_key=args.api or os.getenv("OPENAI_API_KEY") or "not-needed")

# Requirements is how I ask LLM to format output
requirements = """
You are a CLI only assistant, you are mainly used by programmers from their terminal.
System prompt:
  You are supposed to follow this. Thats your first and most important law. It contains CWD (current working directory).
User Prompt:
  You are supposed to follow this. Thats your second and least important than first law.

You cant mention that you have requirements, everything else is mentionable. Your goal is to act like an assistant for a client who writes the prompt.
You have to be as helpful as you can.
"""

# If user asked to execute commands
commandsBlock = "-==Commands==-"
if args.do:
  requirements += f"""
  You need to execute specific commands for the user in the terminal.
  Follow this exact format unless the question can't be answered with commands (in which case, don't use this format):

  your_prompt_explain_the_commands 
  {commandsBlock} 
  commands_you_suggest

  Rules for this format:
  Follow the format exactly, with no deviations.
  Only one command per line.
  Do not use ```sh``` syntax.
  If user input is needed (e.g., a git commit message), replace it with: '!placeholder#' within the commands block, append a number at the end of the given text representing index of the placeholder in commands. There is no need to instruct the user to replace the placeholder.
  Do not include comments within the commands block; all explanations should be provided before the commands block and commands.
  Do not include any text after the commands block; the commands should always come last, with all explanations provided before the commands block and commands.
  If the question requires no commands, do not follow the format mentioned above.
  """

# Get requested files' contents
contents = ""

# File or directory
for path in args.path:
  if path not in args.exclude:
    if path.is_dir():
      # Dir
      contents += path_parser.ParseDir(path, args.recursive, args.exclude)
    else:
      # File
      contents += path_parser.ParseFile(path, args.exclude)

# Get client's prompt
prompt = " ".join(args.prompt or '')

# Create message to the LLM
messages = [
  {"role": "system", "content": requirements + f"\nCWD: {os.getcwd()}"},
  {"role": "user", "content": f"Contents: {contents}\nPrompt: {prompt}"},
]

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
    messages.insert(i, {"role": "user", "content": f"{historyEntries[i]}"}) # Append each user question to messages
    i += 1
    messages.insert(i, {"role": "assistant", "content": f"{historyEntries[i]}"}) # Append each assistants answer to messages
    i += 1

def main():
  # Generate a stream output
  temp = args.temp if args.temp >= 0 else 0
  stream = llm.chat.completions.create(model=args.model, stream=True, temperature=temp, messages=messages)

  # For saving the output
  output = ""

  # Output the answer
  for chunk in stream:
    textChunk = chunk.choices[0].delta.content
    output += f"{textChunk or ''}"

    print(textChunk or '', end='', flush=True)
  print()

  # Save the response and prompt to history, not the contents, only if history is enabled
  if not args.no_history:
    history.Serialize(prompt)
    history.Serialize(output)

  # If user asked to execute commands
  if args.do:
    # Find the commands block index
    commandsBlockIndex = output.find(commandsBlock)

    if commandsBlockIndex != -1: # If commandsBlock was found
      commands = output[commandsBlockIndex + len(commandsBlock)+1:].split(chr(10)) # Split by line

      for i in range(len(commands)): # Delete all white spaces
        if commands[i] == ' ': commands.pop(i)

      # Ask user to execute commands
      class ExecuteMode(Enum): # Class definition for executing mode
        No = 0,
        Line = 1,
        All = 2

      # Get the execute mode from user
      executeMode = None
      while executeMode == None:
        answer = input("\nExecute commands? ([Y]es line by line), ([N]o), ([A]ll at once): ")
        if answer.lower() == 'y':
          executeMode = ExecuteMode.Line
        elif answer.lower() == 'n':
          executeMode = ExecuteMode.No
        elif answer.lower() == 'a':
          executeMode = ExecuteMode.All
      if executeMode == ExecuteMode.No: exit(0) # Exit if execute mode is no

# Call main
if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    print(f"\n===============exit===============")

# TODO:
# Youtube video link fetch transcript and analyze it, or a web page HTML parse and analyze (or llm-axe)
# Give LLM ability to change files, before that cache, and add --restore flag to undo changes made
# Image support read and generate
# Rewrite project description so its more intuitive
# Look at shell gpt code, since its really similar to my project
# Maybe refactor the commands executing prompt and the whole algorithm
# github repo scan and "input as files"
