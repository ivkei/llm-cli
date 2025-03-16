# llm-cli
This project allows CLI use of LLMs through any server that supports OpenAI API format of hosting LLMs.  
I used the program with llama.cpp's server.  

# Features
* Get responses from terminal.
* Input files and whole directories into LLMs for them to read.
* Requires absolutely no GUI to install and use.  
* History of conversations

# Installation
## Prerequisites
* [git](https://git-scm.com/)
* [python](https://www.python.org/)
* pip, comes with python
* (Optional) python-venv, comes with python

## Without venv:
### Cross platform way:
```sh
git clone https://github.com/debugkei/llm-cli
cd llm-cli
pip install -r requirements.txt
```
## With venv:
### Linux:
```sh
git clone `https://github.com/debugkei/llm-cli`  
cd llm-cli  
python -m venv  
source venv/bin/activate  
pip install -r requirements.txt  
```
### Windows:
```sh
git clone `https://github.com/debugkei/llm-cli`  
cd llm-cli  
python -m venv  
venv\Scripts\activate  
pip install -r requirements.txt  
```

# Usage
```sh
python src/llm-cli.py -p your prompt
```
`-m` - name of the model on the server, if not specified uses `default`.  
`-u` - url of the server, if not specified uses `http://localhost:8080`.  
`-w` - paths for LLM to consider and read.  
`-r` - If provided with directories then read all files inside recursively, if flag isnt set then dont read recursively.  
`-e` - Exclude specific paths that LLM is not going to consider.  
`-t` - set the temperature for the LLM. Range 0-1, where 0 - be straight forward.  
`-a` - API, can be either specified, if not uses enviroment variable `OPENAI_API_KEY`, else assumed that API is not needed (running locally).  
  If API is not needed but envoriment variable has to stay, then use `-a not-needed`.  
`-h` - print out possible flags with their description.  
`-n` - disables history just for one message and turns it back on after.  
`-c` - clears the history.  
`-l` - specifies the length of history remembered, default is 3 previous conversations.  

Some CLIs dont allow special characters such as `()`, if so then just wrap the prompt into `""`.  

## Usage example with llama.cpp
1. Download precompiled binary from [here](https://github.com/ggml-org/llama.cpp/releases) for your platform and GPU rendering API.  
  Or to download via terminal:
  ```sh
  git clone https://github.com/ggml-org/llama.cpp
  ```
  And then build it, how to build is [here](https://github.com/ggml-org/llama.cpp#building-the-project)  
2. Download a model from [here](https://huggingface.co/)  
3. Start the server:  
```sh
cd to/your/llama.cpp/installation  
./llama-server -m /path/to/your/model.gguf -c 2048 -ngl 200  
```
`-ngl` - amount of work offloaded to gpu, everything above 100 is 100, and if you planning on using CPU, then just dont include -ngl.  
`-c` - context, for bigger prompts, files or directories use greater values.  
4. [Usage](#usage)  
  * Not need to specify the URL because default URL of ./llama-server is `http://localhost:8080`.  
  * If multimodel server then in usage specify the model, else if only 1 model is hosted then default will handle the job.
  * API is not needed so just dont set the flag

# Deletion
1. Delete the directory with llm-cli.  
2. Delete the alias, if created. Just erase it from .bashrc, or .zshrc, or from $PROFILE.

# Dependencies
## To install all
```sh
pip install -r requirements.txt  
```
## List
* openai (python package)
* os (python package, builtin)
* pathlib (python package, builtin)
* argparse (python package, builtin)

# Important details
Dont change the project's architecture because history may stop working because it depends on parent directory of directory with src.  
The history doesnt save the contents of previous files given to LLM, it does save only user's prompts and LLM's output.  

# Development
### This project is actively developed right now.
* No pull requests will be accepted.
* I didnt figure out yet what to do with venv dependency to launch
