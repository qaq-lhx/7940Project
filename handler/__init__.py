from typing import TYPE_CHECKING, Union, Callable

if TYPE_CHECKING:
    from chatbot import Chatbot


class GetChatbot:
    def __init__(self):
        self.chatbot: Union['Chatbot', None] = None
        self.on_receive = Union[Callable[['Chatbot'], None], None]

    def __call__(self, *args, **kwargs) -> 'Chatbot':
        return self.chatbot
