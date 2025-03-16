import cl_parser
import path_parser
from openai import OpenAI
import os
import history

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
    messages.insert(i, {"role": "user", "content": f"{historyEntries[i]}"}) # Append each assistants answer to messages
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

# Call main
if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    print(f"\n===============exit===============")

# TODO:

# IDEAS:
# Youtube video link fetch transcript and analyze it, or a web page HTML parse and analyze
# Give LLM ability to change files, before that cache, and add --restore flag to undo changes made
# Image support read and generate
