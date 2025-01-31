# LMStudio_Client

LMStudio_Client is a simple Python wrapper for the LMStudio API. Currently, it provides access to the `chat/completions` endpoint, allowing for both blocking and streaming interactions with an LLM running in LMStudio.

## Features
- Supports synchronous (blocking) chat responses.
- Supports streamed responses for real-time interaction.
- Easy-to-use interface for interacting with LMStudio.

## Installation
```sh
pip install lmstudio_client  # (if available as a package)
```
Or clone this repository and install dependencies manually:
```sh
git clone https://github.com/eiredynamic/lmstudio-client-python
cd lmstudio-client-python
```
Ideally also using a venv...
```sh
python -m venv ./venv
```
Install the dependencies
```sh
pip install -r requirements.txt
```
...and install the module locally
```sh
pip install -e .
```

## Usage
A demonstration of how to use the client is available in `example.py`, a simple console-based application.

### Main Functions

```python
def chat(self, usr_prompt, sys_prompt=_sys_prompt, endpoint_root=_endpoint_root, include_reasoning=False):
    """
    Sends a user prompt to the LMStudio API and returns the complete response.
    
    :param usr_prompt: The user input text.
    :param sys_prompt: (Optional) System prompt to guide the model.
    :param endpoint_root: (Optional) Root endpoint of the API.
    :param include_reasoning: (Optional) Whether to include model reasoning, if the model support it.
    :return: The full response from the LLM.
    """
```

```python
def stream_chat(self, usr_prompt, sys_prompt=_sys_prompt, endpoint_root=_endpoint_root, include_reasoning=False):
    """
    Sends a user prompt to the LMStudio API and returns a streamed response.
    
    :param usr_prompt: The user input text.
    :param sys_prompt: (Optional) System prompt to guide the model.
    :param endpoint_root: (Optional) Root endpoint of the API.
    :param include_reasoning: (Optional) Whether to include model reasoning, if the model support it.
    :yield: Streamed response chunks from the LLM.
    """
```

### Example Usage
#### Blocking Call
```python
from lmstudio_client.client import Client

client = Client()
response = client.chat("Tell me a joke.")
print(response)
```

#### Streaming Call
```python
response_stream = client.stream_chat("Tell me a joke.")
for chunk in response_stream:
    print(chunk, end="", flush=True)
```
## Project Repo
https://github.com/eiredynamic/lmstudio-client-python

## License
This project is licensed under the MIT License. See `LICENSE` for details.

## Contributions
Contributions are welcome! Feel free to submit a pull request or report issues.

## Acknowledgments
Thanks to LMStudio for providing the API interface.