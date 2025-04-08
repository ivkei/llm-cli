from pathlib import Path
from paths import GetOSAppDir
import paths

# History limit
historyLimit = 6

# Separator that is going to separate the history entries
separator = "###%%#$TLISFH#\n"

# History entries, list representantion of file contents without separators, used as cache
__historyEntries = []

# History file path
historyFilePath = GetOSAppDir(".history")/"history" # Overriden in main.py

def __deserialize():
  """Deserializes on init for the only time. Dont call after."""

  # If file doesnt exist - create
  if not historyFilePath.exists():
    paths.CreatePath(historyFilePath)

  # Read from file
  with open(file=historyFilePath) as history:
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
        if len(__historyEntries) >= historyLimit and i >= historyLimit: # If the file's history exceeding the history
          __historyEntries.pop(0) # Just dont include exceeding history, it will later be overwritten
        i += 1

def Deserialize():
  """Returns the history of entries, ordered in time, 1st is the oldest"""
  __deserialize()
  return __historyEntries

def Serialize(strConvertable):
  """Write an entry to a history file"""
  # Pop exceeding history limit entry
  while (len(__historyEntries) >= historyLimit and len(__historyEntries) != 0):
    __historyEntries.pop(0)

  # Append to history entries
  __historyEntries.append(f"{strConvertable}")

  # Append to history file
  with open(file=historyFilePath, mode="w") as history:
    for i in range(len(__historyEntries)):
      # Write entry with separator
      history.write(__historyEntries[i] + separator)

def ClearHistory():
  __historyEntries.clear()
  with open(file=historyFilePath, mode="w") as history:
    history.truncate(0)
