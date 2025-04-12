"""
This module is just an abstraction to talk with openai server.
This module has set of function to use by clients.
Before talking to server it has to get init by Init function.
Then Prompts can be attached and then response can be fetched.
"""
from openai import OpenAI

# Create message to the LLM
__messages = []

# Create llm instance
__llm = []

def Init(url, api):
  """Initializes the library with the server and API.
  Necessary for library to function

  Parameters
  ----------
  url is a url to the server that supports OpenAI API format.
  api is API needed to access the server, pass 'not-needed' to ignore (for local llamas)."""

  __llm.append(OpenAI(base_url=url, api_key=api))

def AddSystemPropmt(prompt):
  """Adds the system propmt to a request. Sorted by time added. The first added is earlier system prompt."""
  __messages.append({"role": "system", "content": prompt})

def AddUserPropmt(prompt):
  """Adds the user propmt to a request. Sorted by time added. The first added is earlier system prompt."""
  __messages.append({"role": "user", "content": prompt})

def AddAssistantPropmt(prompt):
  """Adds the assistant propmt to a request. Sorted by time added. The first added is earlier system prompt."""
  __messages.append({"role": "assistant", "content": prompt})

def Respond(model="default", isStreaming=True, temperature=0.7):
  """Responds to specified via AddPrompt functions prompt. Returns either a stream if said so, or a response,
  on info how to use both go to openai python package documentation (https://github.com/openai/openai-python).
  
  Parameters
  ----------
  model is the name of a model on a server to access, by default accesses the default one.
  isStreaming dictates whether response is streaming or no.
  temperature defines the temperature of the response.
  """
  return __llm[0].chat.completions.create(model=model, stream=isStreaming, temperature=temperature, messages=__messages)

def PrintRespond(model="default", isStreaming=True, temperature=0.7, doIgnoreTripleBacktick=False):
  """Prints the response to prompt specified via AddPrompt functions. Returns the output of the LLM."""
  response = Respond(model=model, isStreaming=isStreaming, temperature=temperature)

  # For saving the output
  output = ""

  if isStreaming:
    # Output the answer
    isIgnoringTheLine = False
    for chunk in response:
      textChunk = chunk.choices[0].delta.content

      # Ignore triple backtick
      if textChunk and "```" in textChunk and doIgnoreTripleBacktick: # Start ignoring the line if found ``` and ignore triple backtick is True
        isIgnoringTheLine = True

      if textChunk and isIgnoringTheLine and chr(10) in textChunk: # Stop ignoring the line if reached the end
        isIgnoringTheLine = False
        continue

      if isIgnoringTheLine: continue # Ignore the line

      # Save to output
      output += f"{textChunk or ''}"

      print(textChunk or '', end='', flush=True)

  else:
    output = response.choices[0].message.content 

    if doIgnoreTripleBacktick:
      # Delete all lines with triple backticks
      lines = output.splitlines()

      for i in range(len(lines)):
        if lines[i].startswith("```"):
          lines.pop(i)
      
      output = "".join(lines)

    print(output, end = '') # Print

  # Return the output
  return output

def ClearPrompts():
  __messages.clear()

def ClearSystemPrompts():
  for i in range(len(__messages)):
    if i < len(__messages) and __messages[i]["role"] == "system":
      __messages.pop(i)
