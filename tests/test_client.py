import pytest
from lmstudio_client.chat_service import InvalidURLException

@pytest.fixture
def test_client(scope="module"):
    from lmstudio_client.chat_service import DummyChatService
    from lmstudio_client.client import Client
    return Client(DummyChatService())

class TestLMStudioClientMethods():
    _endpoint_root = "http://localhost:1234/v1/"
    _expected_endpoint = "http://localhost:1234/v1/chat/completions"
    _endpoint_suffix = "/chat/completions"

    def test_upper(self):
        assert 'foo'.upper() == 'FOO'
    
    def test_no_trailing_slash(self, test_client):
        assert test_client.build_endpoint(str(self._endpoint_root).rstrip('/')) == self._expected_endpoint

    def test_trailing_slash(self, test_client):
        assert test_client.build_endpoint(self._endpoint_root) == self._expected_endpoint

    def test_stream_chat_async_required_params_should_return_expected_strings(self, test_client):
        # Arrange
        expected = "HelloWorld{_expected_endpoint}False".format(_expected_endpoint=self._expected_endpoint)
        # Act
        actual = test_client.chat_async("Hello World")
        # Assert
        assert expected == actual

    # @pytest.mark.asyncio
    def test_stream_chat_async_optional_params_should_return_expected_strings(self, test_client):
        # Arrange
        result = ""
        expected = "HelloWorld{_expected_endpoint}True".format(_expected_endpoint=self._expected_endpoint)
        gen = test_client.stream_chat_async("Hello World", "You are a helpful assistant", "http://localhost:1234/v1/", True)
        for response in gen:
            result += response
        # Act
        actual = result
        # Assert
        assert expected == actual

    def test_chat_async_required_params_should_return_expected_strings(self, test_client):
        # Arrange
        expected = "HelloWorld{_expected_endpoint}False".format(_expected_endpoint=self._expected_endpoint)
        # Act
        actual = test_client.chat_async("Hello World")
        # Assert
        assert expected == actual

    def test_chat_async_optional_params_should_return_expected_strings(self, test_client):
        # Arrange
        expected = "HelloWorld{_expected_endpoint}True".format(_expected_endpoint=self._expected_endpoint)
        # Act
        actual = test_client.chat_async("Hello World", "You are a helpful assistant", "http://localhost:1234/v1/", True)
        # Assert
        assert expected == actual

    def test_chat_client_should_catch_bad_uris(self, test_client):
        _endpoint_root = "test"
        with pytest.raises(InvalidURLException) as ex:
            test_client.chat_async("Hello", endpoint_root=_endpoint_root)
        assert str(ex.value) == (f"Invalid URL: {_endpoint_root + self._endpoint_suffix}")