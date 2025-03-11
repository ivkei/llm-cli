import argparse

# Create arg parser
parser = argparse.ArgumentParser("Argument parser for llm_cli.py.")

# Add all necessary args
parser.add_argument("url", help="The LLM server url.", type=str)
parser.add_argument("model", help="The name of the model that is going to be used from the server.", type=str)

parser.add_argument("-d", "--dir", help="The directory for LLM to read.")
parser.add_argument("-f", "--file", help="The file for llm to read.")
parser.add_argument("-t", "--temp", help="The temperature of LLM's response.")

parser.add_argument("prompt", help="User's prompt", nargs='*')

def GetArgs():
  """This function returns an object with attributes of parsed arguments."""
  return parser.parse_args()