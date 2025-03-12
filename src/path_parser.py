def ParseDir(path, recursive, excludes):
  contents = ""
  for path in path.iterdir():
    if path.is_dir():
      # Dir
      if recursive and path not in excludes:
        # Parse if needed
        contents += ParseDir(path, recursive, excludes)
    else:
      # File
      contents += ParseFile(path, excludes)
  return contents

def ParseFile(path, excludes):
  if path in excludes: return
  with path.open('r', errors="ignore") as file:
    return f"Filename: {file.name}\nContents: {file.read()}\n"