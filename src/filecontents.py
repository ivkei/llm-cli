def GetDirContents(path, recursive, excludes : list) -> str:
  """Parses a directory and concatenates all file contents into 1, with ParseFile's format, either recursively and with ability to exclude files or dirs."""
  contents = ""
  for path in path.iterdir():
    if path.is_dir():
      # Dir
      if recursive and path not in excludes:
        # Parse if needed
        contents += GetDirContents(path, recursive, excludes)
    else:
      # File
      contents += GetFileContents(path, excludes)
  return contents

def GetFileContents(path, excludes : list) -> str:
  """Parses a file and returns its contents in following format: \"Filename: {file.name}\\nContents: {file.contents}\\n\""""
  if path in excludes: return ""
  with path.open('r', errors="ignore") as file:
    return f"Filename: {file.name}\nContents: {file.read()}\n"
