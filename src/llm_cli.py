import cl_parser
from openai import OpenAI

def main():
  args = cl_parser.GetArgs()

  # Create llm server access instance
  llm = OpenAI(base_url=args.url, api_key="not-needed")

  # File or directory
  if "dir" in args.__dict__:
    pass
  elif "file" in args.__dict__:
    pass

  stream = llm.chat.completions.create(model=args.model, stream=True,
    messages=[{"role": "user", "content": "".join(args.prompt)}],
    )

  for chunk in stream:
    print(chunk.choices[0].delta.content or '', end='', flush=True)
  print()

if __name__ == "__main__":
  try:
    main()
  except Exception as e:
    print("\033[31m", "Error: ", "{ ", e, " }", "\033[0m", sep='')

# TODO:
# Add API key argv
# Argv parameters docs
# Render in markdown??