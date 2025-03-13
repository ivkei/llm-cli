import argparse
from pathlib import Path

# Create arg parser
parser = argparse.ArgumentParser()

# Add all necessary args
parser.add_argument("-u", "--url", help="The LLM server url.", type=str, default="http://localhost:8080")
parser.add_argument("-m", "--model", help="The name of the model that is going to be used from the server.", type=str, default="default")

parser.add_argument("-a", "--api", help="The API for a model, only specify if not running locally.", type=str, default=None)

parser.add_argument("-w", "--path", help="The path or paths for LLM to read. Can either be a file or a directory, if directory additionally -r can be used.",
                     type=Path, nargs="*", default=[])
parser.add_argument("-r", "--recursive", help="Look into directories recursively.", action="store_true")
parser.add_argument("-e", "--exclude", help="Exclude specific directories from showing them to LLM.", nargs='*', default=[], type=Path)

parser.add_argument("-t", "--temp", type=float, 
                    help="The temperature of LLM's response. If not specified then 0.7 is used. The closer to 0 the more straight-forward the output is. The limit is 1.",
                    default=0.7)

parser.add_argument("-p", "--prompt", help="User's prompt", nargs='*')

def GetArgs():
  """This function returns an object with attributes of parsed arguments."""
  return parser.parse_args()