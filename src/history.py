"""
This is generic library for serializing history.
History is stored in a file (path attribute of the module).
It can have a limit (limit attribute of the module).
Its separator in a file can be overriden (separator attribute of the module).
"""
from paths import CreatePath

# History limit
length = 6

# Separator that is going to separate the history entries
separator = "###%%#$TLISFH#\n"

# History entries, list representantion of file contents without separators, used as cache
__historyEntries = []

# History file path
path = None # Errors may occur because its set to None, but programmer has to set the path first

def __Deserialize():
  """Deserializes on init for the only time. Dont call after."""

  # If file doesnt exist - create
  if not path.exists():
    CreatePath(path)

  # Read from file
  with open(file=path) as history:
    i = 0
    for line in history:
      # Search for separator
      idx = line.find(separator)

      # Part of line to deserialize, exists for separators
      linePartToDeserialize = line if idx == -1 else line[:idx]

      # Append or concatenate
      if i < len(__historyEntries):
        __historyEntries[i] += linePartToDeserialize
      else:
        __historyEntries.append(linePartToDeserialize)
              
      # If we reached the separator then increase the current entry index
      if idx != -1: # If found
        if len(__historyEntries) >= length and i >= length: # If the file's history exceeding the history
          __historyEntries.pop(0) # Just dont include exceeding history, it will later be overwritten
        i += 1

def Deserialize():
  """
  Returns the history of entries, ordered in time, 1st is the oldest
  Assumes the path attribute of the module was set properly.
  """
  __Deserialize()
  return __historyEntries

def Serialize(strConvertable):
  """Write an entry to a history file"""
  # Pop exceeding history limit entry
  while (len(__historyEntries) >= length and len(__historyEntries) != 0):
    __historyEntries.pop(0)

  # Append to history entries
  __historyEntries.append(f"{strConvertable}")

  # Append to history file
  with open(file=path, mode="w") as history:
    for i in range(len(__historyEntries)):
      # Write entry with separator
      history.write(__historyEntries[i] + separator)

def Clear():
  __historyEntries.clear()
  with open(file=path, mode="w") as history:
    history.truncate(0)
