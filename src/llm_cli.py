from llama_cpp import Llama
from cl_parser import GetArgs

args = GetArgs()

# Validate url

# File or directory
if "dir" in args.__dict__:
  pass
elif "file" in args.__dict__:
  pass

print(args.url)