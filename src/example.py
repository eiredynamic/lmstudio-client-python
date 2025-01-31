from lmstudio_client.client import Client

if __name__ == '__main__':
    client = Client()
    response = client.chat("Ask me a riddle!", "You are a helpful assistant", "http://localhost:1234/v1/", False)
    print(response)

    print("\n\n")

    for response in client.stream_chat("Give me a poem about cats!", "You are a helpful assistant", "http://localhost:1234/v1/", True):
        print(response, end='', flush=True)


