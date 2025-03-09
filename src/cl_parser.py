import argparse

# Create arg parser
parser = argparse.ArgumentParser("Argument parser for llm_cli.py.")

# Add all necessary args
parser.add_argument("url", help="The llama.cpp server url.", type=str)

parser.add_argument("-d", "--dir", help="The directory for llama.cpp to read.")
parser.add_argument("-f", "--file", help="The file for llama.cpp to read.")

parser.add_argument("prompt", help="User's prompt")

def GetArgs():
  """This function returns an object with attributes of parsed arguments."""
  return parser.parse_args()