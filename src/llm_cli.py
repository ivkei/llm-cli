import cl_parser
from openai import OpenAI

def main():
  args = cl_parser.GetArgs()

  # Create LLM server access instance
  llm = OpenAI(base_url=args.url, api_key=args.api or "not-needed")

  # Contents is additional file contents
  contents = ""

  # Requirements is how I ask LLM to format output
  requirements = """"""

  # File or directory
  if "dir" in args.__dict__:
    pass
  elif "file" in args.__dict__:
    pass
  
  # Generate a stream output
  stream = llm.chat.completions.create(
    model=args.model,
    stream=True,
    temperature=args.temp or 0.7,
    messages=[
              { "role":
                  "user",
                "content":
                  "<<Requirements>>" + requirements + "<<!Requirements>>" +
                  "<<Contents>>" + contents + "<<!Contents>>" +
                  "<<Client's prompt>>" + "".join(args.prompt) + "<<!Client's prompt>>"
              }
             ],
    )

  # Output the answer
  for chunk in stream:
    print(chunk.choices[0].delta.content or '', end='', flush=True)
  print()

# Call main
if __name__ == "__main__":
  # try:
    main()
  # except Exception as e:
  #   print("\033[31m", "Error: ", "{ ", e, " }", "\033[0m", sep='')

# TODO:
# Interruption support
# File or Dir fetching contents support
# Write requirements

# REMEMBER:
# Remember to feed the LLM with current path
# Remind the LLM about mkdir and touch
# Preview the commands LLM is going to execute

# IDEAS:
# Youtube video link fetch transcript and analyze it
# Give LLM ability to change files, before that cache, and add --restore flag to undo changes made