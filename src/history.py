from pathlib import Path
from os import path

# History limit
historyLimit = 6

# Separator that is going to separate the history entries
separator = "###%%#$TLISFH#\n"

# History entries, list representantion of file contents without separators, used as cache
historyEntries = []

# History file path
historyFilePath = Path(f"{path.dirname(__file__)}/../history")

def __deserialize():
  """Deserializes on init for the only time. Dont call after."""
  # If file doesnt exist - create
  open(file=historyFilePath, mode='a').close()

  # Read from file
  with open(file=historyFilePath) as history:
    i = 0
    for line in history:
      # Search for separator
      idx = line.find(separator)

      # Push the line to history entry, if history entry doesnt exist then create one, if separator is present then push until separator
      copyUpTo = idx + (1 if idx == -1 else 0)
      if i < len(historyEntries):
        historyEntries[i] += line[:copyUpTo]
      else:
        historyEntries.append(line[:copyUpTo])
      
      # If we reached the separator then increase the current entry index
      if idx != -1: # If found
        i += 1
__deserialize()

def Deserialize():
  """Returns the history of entries, ordered in time, 1st is the oldest"""
  return historyEntries

def Serialize(strConvertable):
  """Write an entry to a history file"""
  # Pop exceeding history limit entry
  if len(historyEntries) >= historyLimit:
    historyEntries.pop(0)

  # Append to history entries
  historyEntries.append(f"{strConvertable}")

  # Append to history file
  with open(file=historyFilePath, mode="w") as history:
    for i in range(len(historyEntries)):
      # Write entry
      history.write(historyEntries[i])
      
      # Write separator
      history.write(separator)

def ClearHistory():
  historyEntries.clear()
  with open(file=historyFilePath, mode="w") as history:
    history.truncate(0)