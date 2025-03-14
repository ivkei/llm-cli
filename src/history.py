from pathlib import Path

# History limit
historyLimit = 6

# Separator that is going to separate the history entries
separator = "###%%#$TLISFH#\n"

# History entries, list representantion of file contents without separators, used as cache
__historyEntries = []

# History file path
historyFilePath = Path(__file__).parent.parent / "history" # .parent is a parent dir

def __deserialize():
  """Deserializes on init for the only time. Dont call after."""
  # If file doesnt exist - create
  if not historyFilePath.exists():
    historyFilePath.touch()

  # Read from file
  with open(file=historyFilePath) as history:
    i = 0
    for line in history:
      # Search for separator
      idx = line.find(separator)

      # Push the line to history entry, if history entry doesnt exist then create one, if separator is present then push until separator
      copyUpTo = idx + (1 if idx == -1 else 0)
      if i < len(__historyEntries):
        __historyEntries[i] += line[:copyUpTo]
      else:
        __historyEntries.append(line[:copyUpTo])
              
      # If we reached the separator then increase the current entry index
      if idx != -1: # If found
        if len(__historyEntries) >= historyLimit and i >= historyLimit: # If the file's history exceeding the history
          print("popped")
          __historyEntries.pop(0) # Just dont include exceeding history, it will later be overwritten
        i += 1

def Deserialize():
  """Returns the history of entries, ordered in time, 1st is the oldest"""
  __deserialize()
  print(len(__historyEntries))
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
