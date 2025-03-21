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

def PrintRespond(model="default", isStreaming=True, temperature=0.7):
  """Prints the response to prompt specified via AddPrompt functions. Returns the output of the LLM."""
  response = Respond(model=model, isStreaming=isStreaming, temperature=temperature)

  # For saving the output
  output = ""

  if isStreaming:
    # Output the answer
    for chunk in response:
      textChunk = chunk.choices[0].delta.content
      output += f"{textChunk or ''}"

      print(textChunk or '', end='', flush=True)
    print()
  else:
    output = response.choices[0].message.content 
    print(output)

  # Return the output
  return output

def ClearPrompts():
  __messages.clear()

def ClearSystemPrompts():
  for i in range(len(__messages)):
    if __messages[i]["role"] == "system":
      __messages.pop(i)
