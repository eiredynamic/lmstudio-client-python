from lmstudio_client.client import Client

if __name__ == '__main__':
    client = Client()
    for response in client.stream_chat_async("What is the capital of France?", "You are a helpful assistant", "http://localhost:1234/v1/", False):
        print(response, end='')