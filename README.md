# llm-cli
This project allows you to access LLMs right from your terminal, CLI or shell, whatever you want to call it.  
The LLM can be local hosted or it can be any other LLM server that is OpenAI API compatible.  
Optimized for both local and server.  
The only requirement for the application to work is to have a working server that is OpenAI API compatible.  
This project is absolutely cross-platform and can run either via python interpreter or packed into an application (See more: [Usage](#usage)).  
I only tested it with [llama.cpp](https://github.com/ggml-org/llama.cpp) yet, because I dont have an OpenAI API key.  

# Features
* Get responses straight from the shell, terminal or CLI, whatever the name is.
* Feed the LLM with contents of files, or even directories, or even stdouts of other programs, following can be used, | pipe, $() syntax or a -w flag (--help will help).  
* [Installation](#installation) requires absolutely no graphical interface.
* Manipulate the history of conversations any way you want (--help will help).
* Ask LLM to execute commands for you with the knowledge of the OS running.
* Cross-platform as long as [python](https://www.python.org/) is.
* Ask the LLM for code via `-o` flag, and possibly redirect to a file. Maybe even use `:r !llm-cli -p solve me a coin change problem -o` if you use vim or neovim. Or just pipe the output to a pbcopy.  
* Really customizable.  

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
`-w` - paths for LLM to consider and read.  
`-r` - If provided with directories then read all files inside recursively, if flag isnt set then dont read recursively.  
`-e` - Exclude specific paths that LLM is not going to consider.  
`-h` - print out possible flags with their description.  
`-b` - Restores the default config.  
`-c` - clears the history.  
`-s` - asks the LLM to execute commands in right in CLI for you, not recommended to use with LLMs that have below 7b parameters, they may output wrong format.  
`-p` - specify the prompt to LLM.  
`-o` - ask the LLM to produce only code.   
#### Remembered ones - ones that are set once and then reused without setting again
`-m` - name of the model, defaults to default one on the server.  
`-u` - url of the server, defaults to `http://localhost:8080`.  
`-t` - set the temperature for the LLM. Range 0-1, where 0 - be straight forward.  
`-a` - API to access the model on the server, defaults to not-needed, not-needed is for local use, set the flag for server use.  
`-n` - toggles history on and off, defaults to on.  
`-l` - length of the history that is remembered by the LLM, defaults to 3, recommended lower values with lower context windows.  
`-d` - override the directory with history and config, defaults to `~/.llm-cli/`.  
`-f` - toggles between rememembered file contents and not, defaults to remember, recommended to toggle off with lower context windows.  

##### Some CLIs dont allow special characters such as `()`, if so then just wrap the prompt into `""`.  

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
| ❌ | Add usage examples images in README.md |  
| ✅ | LLM modify files |  
| ❌ | Image generation/describing??? |  
| ❌ | Get HTML contents of webpages, transcripts of [Youtube](https://www.youtube.com/) videos, [llm-axe](https://github.com/emirsahin1/llm-axe) can be helpful |  
| ✅ | Setup github actions to auto release |  
| ❌ | Setup github actions to upload project to [PyPi](https://pypi.org) |  
| ✅ | Add option for some flags (Ex: cache-location or url) to be an enviromental variable, or create a config file with values |  
| ❌ | Add code documentation to CONTRIBUTING.md |  
| ❌ | Own argparser, not python builtin |  
| ❌ | User can add a system prompt |  

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
