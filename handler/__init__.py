from typing import TYPE_CHECKING, Callable, Optional

if TYPE_CHECKING:
    from chatbot import Chatbot


class GetChatbot:
    def __init__(self):
        self.chatbot: Optional['Chatbot'] = None
        self.on_receive: Optional[Callable[['Chatbot'], None]] = None

    def __call__(self, *args, **kwargs) -> 'Chatbot':
        return self.chatbot

    def provide(self, chatbot: 'Chatbot') -> None:
        self.chatbot = chatbot,
        if self.on_receive is not None:
            self.on_receive(chatbot)
