from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from chatbot import Chatbot


class GetChatbot:
    def __init__(self):
        self.chatbot = None

    def __call__(self, *args, **kwargs) -> 'Chatbot':
        return self.chatbot
