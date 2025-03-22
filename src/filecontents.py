def GetDirContents(path, recursive, excludes : list) -> str:
  """Parses a directory and concatenates all file contents into 1, with ParseFile's format, either recursively and with ability to exclude files or dirs.

  Parameters
  ----------
  @path@ is path to get contents from.
  @excludes@ are files or directories to not get contents from.
  @recursive@ determines whether to go deep into a directory on no.
  """
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
  """Parses a file and returns its contents in following format: \"Relative Path: {path}\\nContents:\n{file.contents}\"

  Parameters
  ----------
  @path@ is path to get contents from.
  @excludes@ are files to not get contents from.
  """
  if path in excludes: return ""
  with path.open('r', errors="ignore") as file:
    return f"""Relative Path: {path}\nContents:\n{file.read()}
    """

def GetPathsContents(paths : list, excludes : list, recursive):
  """Gets contents of either directories or files at paths with few options.
  
  Parameters
  ----------
  @paths@ are paths to get contents from.
  @excludes@ are files or directories to not get contents from.
  @recursive@ determines whether to go deep into a directory on no.
  """
  # Get requested files' contents
  contents = ""

  # File or directory
  for path in paths:
    if path not in excludes:
      if path.is_dir():
        # Dir
        contents += GetDirContents(path, recursive, excludes)
      else:
        # File
        contents += GetFileContents(path, excludes)

  return contents
