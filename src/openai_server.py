from openai import OpenAI

# Create message to the LLM
__messages = []

def Init(url, api):
  """Initializes the library with the server and API.
  Necessary for library to function

  Parameters
  ----------
  url np.str is a url to the server that supports OpenAI API format.
  api is API needed to access the server, pass 'not-needed' to ignore (for local llamas)."""

  __llm = OpenAI(base_url=url, api_key=api)

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
  return __llm.chat.completions.create(model=model, stream=isStreaming, temperature=temperature, messages=__messages)
