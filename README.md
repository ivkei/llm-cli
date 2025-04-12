# llm-cli
This project allows you to access LLMs right from your terminal, CLI or shell, whatever you want to call it.  
The LLM can be local hosted or it can be any other LLM server that is OpenAI API compatible.  
Optimized for both local and server.  
The only requirement for the application to work is to have a working server that is OpenAI API compatible.  
This project is absolutely cross-platform and can run either via python interpreter or packed into an application (See more: [Usage](#usage)).  
I only tested it with [llama.cpp](https://github.com/ggml-org/llama.cpp) yet, because I dont have an OpenAI API key.  

# Why llm-cli?
* Optimized for both local and server use.
* If running locally even low number of parameters models will do good.
* Has a lot of customization and features, such as executing or feeding the LLM with local data.
* Easy to install.
* Cross-platform.
* Intuitive to use.

# Features
## Responses
* Get responses straight from the shell, terminal or CLI, whatever the name is.
```sh
llm-cli -p Whats coin change problem in dynamic programming?  
# Coin change in dynamic programming is an interesting problem ...  
```

## Files, pipes, and feeding the LLM
* Feed the LLM with contents of files, or use pipes, or how about this: `$()`.  
### Files
```sh
llm-cli -p What is this directory? -w src/ -e src/__pycache__ -r  
# This directory and it subdirectories are part of ...  
```

### Pipe
```sh
cat reminders.txt | llm-cli -p What did I forget to do?  
# For this project you planned on adding ... today  
```

### $()
```sh
llm-cli -p What did I do wrong in the fibonacci implementation? Here: $(cat fibonacci.py)  
# It seems like you didnt ...  
```

## Installation
* No graphical interface to install and setup, if even you use live usb with arch, this program will help you.  
* [Installation](#installation).  

## History
### Want to shrink or expand amount of history saved?
```sh
llm-cli --history-length 25 # 25 previous conversations are remembered  
```

### Want to clear history?
```sh
llm-cli -c
llm-cli -c -p Hello, your name is now Gage! # Or start the new conversation instantly
```

### Want to disable history?
```sh
llm-cli --toggle-history
```

### Want to optimize history for small context windows?
```sh
llm-cli --toggle-limit-history # This will limit the history to only text prompt and text answer (no file contents will be saved)
```

#### For more information on flags go to [here](#usage)

## Commands
* LLM can be asked to execute commands.
```sh
git diff | llm-cli -p Generate me a git commit
# git add .
# git commit -m "..."
[E]xecute, [D]escribe, [A]bort:
```
### Or
* The LLM knows about system, release, time and date, and Current Working Directory.
```sh
llm-cli -p Update my system
# sudo pacman -Syu
[E]xecute, [D]escribe, [A]bort: e
[sudo] password for ... :
```

### Or
```sh
llm-cli -p Start a docker container
# docker ...
[E]xecute, [D]escribe, [A]bort: d
# This commands do ...
```

## Code
* The LLM can be asked to output only code.
```sh
llm-cli -p Solve me that coin change problem -o
# def CoinChange(...):
#  ...
#  ...
```
### Or call that straight from vim
```vim
:r !llm-cli -p Write me a simple python fibonacci function -o
```

## Config
* llm-cli is really configurable and flexible.
## Get config variable
```sh
llm-cli --show ...
```
* Where `...` is a variable name to see. For example `temperature`.

## Set config variable
```sh
llm-cli --temperature ...
```
* Where `...` is a variable value to set. For this variable for example its serialized and used over and over.
* To learn more about what variables are saved for future use go to [here](#usage).

## CLI arguments
* To see all the possible flags either go to [here](#usage) or use `--help` flag.

# Installation
There are multiple options when it comes to using the application:  
* Just install a release from [here](https://github.com/debugkei/llm-cli/releases) and use it.  
* Clone the repository and interpret it everytime via python, how to is [here](#interpret).  
* Clone the repository and build it, how to is [here](#build).  

## Interpret

### Prerequisites
* [git](https://git-scm.com/)
* [python](https://www.python.org/) to execute
* pip, comes with python
* (Optional) python-venv, comes with python

### Installation
1. Clone the repository:  
```sh
git clone https://github.com/debugkei/llm-cli
cd llm-cli
```
2. Download all dependencies (venv can be created optionally):  
```sh
pip install -r requirements.txt
```
3. Then alias or function can be created in shell to execute the file (src/main.py) via interpreter.  

## Build
### Prerequisites
* [git](https://git-scm.com/)
* pip, comes with python
* (Optional) python-venv, comes with python

### Installation
1. Clone the repository:  
```sh
git clone https://github.com/debugkei/llm-cli
cd llm-cli
```
2. Download all dependencies and [pyinstaller](https://github.com/pyinstaller/pyinstaller) (venv can be created optionally):  
```sh
pip install -r requirements.txt
pip install pyinstaller
```
3. Build it:  
```sh
pyinstaller --onefile src/main.py --name llm-cli
```
4. Then result (dist/llm-cli) can be copied to already existing enviroment path or one can be created. Or an alias can be created.  

# Usage

## Configuration
The application can be configured.  
Some settings set values for the LLM, some control internal features, such as history.  

### Recommended way to change configuration
Just use flags to set values, for more consult [this](#flags).  

### Unrecommended way to change configuration
The default config location is ~/.llm-cli/config.py.  
Feel free to explore, because if something breaks `-b` [flag](#flags) can be used to restore original config.  
The variables in the file are just written in python syntax.  

## Run
```sh
llm-cli -p your prompt
```
### Flags
#### Single-use ones
`-w` or `--path` - paths for LLM to consider and read.  
`-r` or `--recursive` - If provided with directories then read all files inside recursively, if flag isnt set then dont read recursively.  
`-e` or `--exclude` - Exclude specific paths that LLM is not going to consider.  
`-h` or `--help` - print out possible flags with their description.  
`-b` or `--default-config` - Restores the default config.  
`-c` or `--clear-history` - clears the history.  
`-s` or `--shell` - asks the LLM to execute commands in right in CLI for you, not recommended to use with LLMs that have below 7b parameters, they may output wrong format.  
`-p` or `--prompt` - specify the prompt to LLM.  
`-o` or `--code` - ask the LLM to produce only code.   
`-v` or `--show` - shows a value of the argument or a config variable, for example to show current configured history length - `-v history_length`, replace all `-` from CLI arguments to _.  
#### Remembered ones - ones that are set once and then reused without setting again
`-m` or `--model` - name of the model, defaults to default one on the server.  
`-u` or `--url` - url of the server, defaults to `http://localhost:8080`.  
`-t` or `--temperature` - set the temperature for the LLM. Range 0-1, where 0 - be straight forward.  
`-a` or `--api` - API to access the model on the server, defaults to not-needed, not-needed is for local use, set the flag for server use.  
`-n` or `--toggle-history` - toggles history on and off, defaults to on.  
`-l` or `--history-length` - length of the history that is remembered by the LLM, defaults to 3, recommended lower values with lower context windows.  
`-f` or `--toggle-limit-history` - toggles between rememembered file contents and not, defaults to remember, recommended to toggle off with lower context windows.  
`-d` or `--md-shell` - toggles markdown syntax when commands are asked to be given. Toggle on for clean commands output, works good with Large LLMs. Toggle off with small LLMs because they will try to describe, and the descirption will be interpreted as a command.
TL;DR: If having problems with output with `-s` flag, just toggle off.  

##### Some CLIs dont allow special characters such as `()`, if so then just wrap the prompt into `""`.  

## Optimization for small LLMs and small context windows
* `-n` - toggle history off, for small context windows.
* `-l` - set the length so a small value as an alternative for above.
* `-f` - toggle limit history, file contents will not be saved.
* `-d` - toggles off to enable markdown syntax in commands output, when LLMs output descriptions for some reasons with commands.

## Usage example with [llama.cpp](https://github.com/ggml-org/llama.cpp)
1. Download precompiled binary from [here](https://github.com/ggml-org/llama.cpp/releases) for your platform and GPU rendering API.  
  Or to download via terminal:
  ```sh
  git clone https://github.com/ggml-org/llama.cpp
  ```
  And then build it, how to build is [here](https://github.com/ggml-org/llama.cpp#building-the-project)  
2. Download a model from [here](https://huggingface.co/) or to download via CLI [stackoverflow discussion](https://stackoverflow.com/questions/67595500/how-to-download-a-model-from-huggingface)  
3. Start the server:  
```sh
cd to/your/llama.cpp/installation  
./llama-server -m /path/to/your/model.gguf -c 2048 -ngl 200  
```
`-ngl` - amount of work offloaded to gpu, everything above 100 is 100, and if you planning on using CPU, then just dont include -ngl.  
`-c` - context, for bigger prompts, files or directories use greater values.  
4. [Usage](#usage)  
  * Not need to specify the URL because default URL of ./llama-server is `http://localhost:8080`.  
  * If multimodel server then in [usage](#usage) specify the model, else if only 1 model is hosted then default will handle the job.
  * API is not needed so just dont set the flag

# Development
* The pull requests with a lot of changes will not be accepted, thats my own project for now.
* Less major TODO is located in src/main.py, it just has some minor TODOs.
## Roadmap/TODO
| State | Action |
| ----- | ------ |
| ✅ | Feeding of files to LLM |  
| ✅ | Executing commands from LLM |  
| ✅ | Releases and packaged application via [pyinstaller](https://github.com/pyinstaller/pyinstaller), or alias use with python |  
| ✅ | Add usage examples images in README.md |  
| ✅ | LLM modify files |  
| ❌ | Image generation/describing??? |  
| ❌ | Get HTML contents of webpages, transcripts of [Youtube](https://www.youtube.com/) videos, [llm-axe](https://github.com/emirsahin1/llm-axe) can be helpful |  
| ✅ | Setup github actions to auto release |  
| ❌ | Setup github actions to upload project to [PyPi](https://pypi.org) |  
| ✅ | Add option for some flags (Ex: cache-location or url) to be an enviromental variable, or create a config file with values |  
| ❌ | Add code documentation to CONTRIBUTING.md |  
| ❌ | Own argparser, not python builtin |  
| ❌ | User can add a system prompt |  
| ✅ | Add --show flag that will show specific config variable value |  

# Dependencies/Vendors/Credits
## To install all
```sh
pip install -r requirements.txt  
```
## Vendor List/Credits
* openai (python package), [LICENSE](https://github.com/openai/openai-python?tab=Apache-2.0-1-ov-file#Apache-2.0-1-ov-file)
* os (python package, builtin), [LICENSE](https://docs.python.org/3/license.html)
* pathlib (python package, builtin), [LICENSE](https://docs.python.org/3/license.html)
* argparse (python package, builtin), [LICENSE](https://docs.python.org/3/license.html)
* platform (python package, builtin), [LICENSE](https://docs.python.org/3/license.html)
* sys (python package, builtin), [LICENSE](https://docs.python.org/3/license.html)
* subprocess (python package, builtin), [LICENSE](https://docs.python.org/3/license.html)
* python, [LICENSE](https://docs.python.org/3/license.html)
* pip, [LICENSE](https://github.com/pypa/pip?tab=MIT-1-ov-file#readme)
* pyinstaller (used to build), [LICENSE](https://github.com/pyinstaller/pyinstaller#License-1-ov-file)
* llama.cpp (used to host a server), [LICENSE](https://github.com/ggml-org/llama.cpp#MIT-1-ov-file)
* datetime (python package, builtin), [LICENSE](https://docs.python.org/3/license.html)
