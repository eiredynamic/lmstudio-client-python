import requests
import json
import time
from urllib.parse import urlparse
from abc import ABC, abstractmethod

class InvalidURLException(ValueError):
    """Exception raised for invalid URLs."""
    pass

class IChatService(ABC):
    @abstractmethod
    def chat(self, usr_prompt: str, sys_promt: str, endpoint: str, include_reasoning: bool):
        """Abstract method for chat interaction."""
        pass

    @staticmethod
    def is_valid_url(url):
        """Checks if a given string is a valid URL."""
        parsed = urlparse(url)
        return all([parsed.scheme, parsed.netloc])

class ConcreteChatService(IChatService):
    def __init__(self):
        self.session = requests.Session()

    def chat(self, usr_prompt, sys_promt, endpoint, include_reasoning):
        """
        Sends a chat request to a locally running LM Studio server and streams the response.

        :param usr_prompt: The user's input message.
        :param sys_promt: The system message (context for the model).
        :param endpoint: The LM Studio server URL, e.g., 'http://localhost:1234/v1/chat/completions'.
        :param include_reasoning: Boolean flag to include/exclude reasoning content.
        :yield: The streamed response content.
        """
        
        if self.is_valid_url(endpoint) == False:
            raise InvalidURLException(f"Invalid URL: {endpoint}")
        
        _headers = {"Content-Type": "application/json"}
        _payload = {
             "messages": [
                {"role": "system", "content": sys_promt},
                {"role": "user", "content": usr_prompt}
            ],
            "stream": True
        }
        
        with self.session.post(endpoint, headers=_headers, json=_payload, timeout= 60, stream=True) as r:
            # Check for errors
            r.raise_for_status()
            skip_output = False

            for line in r.iter_lines(decode_unicode=True):
                # Skip empty lines
                if not line:
                    continue
                
                # SSE data is usually prefixed with 'data: '
                if line.startswith("data: "):
                    data_str = line[len("data: "):]
                    
                    # The server may send [DONE] once the stream is complete
                    if data_str.strip() == "[DONE]":
                        break
                    
                    # Otherwise, parse the JSON data in the chunk
                    try:
                        data_json = json.loads(data_str)
                    except json.JSONDecodeError:
                        continue  # or handle error
                    
                    if "choices" in data_json:
                        delta = data_json["choices"][0].get("delta", {})
                        content = delta.get("content", "")
                        # If reasoning is not included, skip the reasoning part
                        if not include_reasoning:
                            if "<think>" in content:
                                skip_output = True
                            elif "</think>" in content:
                                skip_output = False
                                continue
                    # Print or otherwise handle partial tokens as they stream in
                    if not skip_output and content:
                        yield content

class DummyChatService(IChatService):
    def chat(self, usr_prompt, sys_promt, endpoint, include_reasoning):
        """
        Dummy implementation of chat service for testing purposes.
        """
        if self.is_valid_url(endpoint) == False:
            raise InvalidURLException(f"Invalid URL: {endpoint}")
        print("This is a dummy chat client. It does not interact with a server.")
        for word in usr_prompt.split(" "):
            yield word
            time.sleep(0.5)
            
        yield endpoint
        yield str(include_reasoning)
