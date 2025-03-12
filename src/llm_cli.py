import cl_parser
import path_parser
from openai import OpenAI
from os import getcwd

def main():
  args = cl_parser.GetArgs()

  # Create LLM server access instance
  llm = OpenAI(base_url=args.url, api_key=args.api)


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
  
  # Files contents
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

  

  # Generate a stream output
  stream = llm.chat.completions.create(
    model=args.model,
    stream=True,
    temperature=args.temp,
    messages= [
                {"role": "system", "content": requirements + f"\nCWD: {getcwd()}"},
                {"role": "user", "content": f"Contents: {contents}\nPrompt: {" ".join(args.prompt)}"},
              ],
    )

  # Output the answer
  for chunk in stream:
    print(chunk.choices[0].delta.content or '', end='', flush=True)
  print()

# Call main
if __name__ == "__main__":
  main()

# TODO:
# Interruption support
# Previous prompt and answer remembering (session support, only once specify the requirements)
# Make openai api key an enviromental variable

# REMEMBER:
# Remind the LLM about mkdir and touch
# Preview the commands LLM is going to execute

# IDEAS:
# Youtube video link fetch transcript and analyze it
# Give LLM ability to change files, before that cache, and add --restore flag to undo changes made
# Give LLM ability to execute commands right in terminal
# Image support