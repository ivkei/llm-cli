import cl_parser
import path_parser
from openai import OpenAI
import os

def main():
  args = cl_parser.GetArgs()

  # Create LLM server access instance
  llm = OpenAI(base_url=args.url, api_key=args.api)


  # Requirements is how I ask LLM to format output
  requirements = """
  You are a CLI only assistant, you are mainly used by programmers.
  You have <<Requirements>>requirements<<!Requirements>> that tell you what you have to do in the first case.
  Then you have <<Contents>>contents<<!Contents>> that gives you the file's or files' contents in following format:
    <<Filename>>name<<!Filename>><<Contents>>contents<<!Contents>>, there may be multiple files,
    if contents is empty then just ignore it, you can mention parts of contents and if asked by prompt explicilty give the code of it,
    if the contents is unreadable just skip it.
  Also you have the CWD (current working directory).
  Lastly you have prompt <<Client's prompt>>prompt<<!Client's prompt>> your goal is to answer it by using contents (only if contents can be used to give an answer).
  Dont mention requirements that you have. Contents, prompt and CWD can be freely mentioned. If the contents doesnt provide or answer the prompt then you dont mention contents at all.
  Dont forget that client's answer is most important to answer, first always remember to look into contents, and then if the answer cant be made via contents then ignore contents.
  If client asks about files or directories then pretend like he provided you with them.
  """
  
  # Contents is additional file contents
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
    messages=[
              { "role":
                  "user",
                "content":
                  "<<Requirements>>" + requirements + "<<!Requirements>>" +
                  "<<Contents>>" + contents + "<<!Contents>>" +
                  "<<CWD>>" + os.getcwd() + "<<!CWD>>" +
                  "<<Client's prompt>>" + " ".join(args.prompt) + "<<!Client's prompt>>"
              }
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
# Previous prompt and answer remembering
# Rewrite requirements

# ISSUES:
# The "content": is cut for some reasons when long contents of files is inputted

# REMEMBER:
# Remind the LLM about mkdir and touch
# Preview the commands LLM is going to execute

# IDEAS:
# Youtube video link fetch transcript and analyze it
# Give LLM ability to change files, before that cache, and add --restore flag to undo changes made
# Give LLM ability to execute commands right in terminal
# Image support