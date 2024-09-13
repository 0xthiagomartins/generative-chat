import pytest
from src.generative_chat.chat_logic import ChatBot


def test_chatbot_initialization():
    chatbot = ChatBot()
    assert chatbot is not None
    assert hasattr(chatbot, "get_response")


def test_chatbot_response():
    chatbot = ChatBot()
    response = chatbot.get_response("Hello, how are you?")
    assert isinstance(response, str)
    assert len(response) > 0


# Add more tests as needed
