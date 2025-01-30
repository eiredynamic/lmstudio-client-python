from lmstudio_client.chat_service import IChatService, ConcreteChatService

class Client:
    """A client for interacting with LM Studio API."""

    _sys_promt = "You are a helpful assistant."
    _endpoint_root = "http://localhost:1234/v1/"
    _endpoint_suffix = "/chat/completions"
    _chat_service = IChatService

    def __init__(self, chat_service: IChatService = None):
        """Initialize the instance vars & client with the correct service implementation."""
        self._chat_service = ConcreteChatService() if chat_service is None else chat_service

    def build_endpoint(self, endpoint_root):
        """Build the endpoint URL for the LM Studio server."""
        endpoint_root = str(endpoint_root).rstrip('/')
        return endpoint_root + self._endpoint_suffix
    
    def chat(self, usr_prompt, sys_prompt = _sys_promt, endpoint_root = _endpoint_root, include_reasoning = False):
        """Send messages to a locally running LM Studio server and stream the response."""
        result = ""
        for response in self._chat_service.chat(usr_prompt, sys_prompt, self.build_endpoint(endpoint_root), include_reasoning):
            result += response
        return result

    def stream_chat(self, usr_prompt, sys_prompt = _sys_promt, endpoint_root = _endpoint_root, include_reasoning = False):
        for response in self._chat_service.chat(usr_prompt, sys_prompt, self.build_endpoint(endpoint_root), include_reasoning):
            yield response

