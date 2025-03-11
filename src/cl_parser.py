import argparse
import pathlib

# Create arg parser
parser = argparse.ArgumentParser("Argument parser for llm_cli.py.")

# Add all necessary args
parser.add_argument("url", help="The LLM server url.", type=str)
parser.add_argument("model", help="The name of the model that is going to be used from the server.", type=str)

parser.add_argument("-a", "--api", help="The API for a model, only specify if not running locally.", type=str)

parser.add_argument("-d", "--dir", help="The directory for LLM to read.", type=pathlib.Path)
parser.add_argument("-f", "--file", help="The file for llm to read.", type=argparse.FileType('r'))
parser.add_argument("-t", "--temp", type=int, help="The temperature of LLM's response. If not specified then 0.7 is used. The closer to 0 the more straight-forward the output is.")

parser.add_argument("prompt", help="User's prompt", nargs='*')

def GetArgs():
  """This function returns an object with attributes of parsed arguments."""
  return parser.parse_args()