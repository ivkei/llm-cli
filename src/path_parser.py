def ParseDir(path, recursive, excludes) -> str:
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

def ParseFile(path, excludes) -> str:
  if path in excludes: return
  with path.open(errors="ignore") as file:
    return f"<<Filename>>{file.name}<<!Filename>><<Contents>>{file.read()}<<!Contents>>"