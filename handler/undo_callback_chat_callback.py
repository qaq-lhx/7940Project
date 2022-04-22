from telegram import Update
from telegram.ext import CallbackContext

from callback_utils import undo_callback_chat, undo_callback_chat_all_by_chat_id
from handler import GetChatbot


def undo_callback_chat_callback(query, query_data, update: Update, context: CallbackContext):
    if 'callback_chat_instance' in query_data:
        callback_chat_instance = query_data['callback_chat_instance']
    else:
        callback_chat_instance = None
    if 'chat_id' in query_data:
        chat_id = query_data['chat_id']
    else:
        chat_id = None
    if 'then_call' in query_data:
        then_call = query_data['then_call']
    else:
        then_call = None
    if 'then_call_with_data' in query_data:
        then_call_with_data = query_data['then_call_with_data']
    else:
        then_call_with_data = None
    if callback_chat_instance is not None:
        undo_callback_chat(callback_chat_instance, chatbot().db)
    elif chat_id is not None:
        undo_callback_chat_all_by_chat_id(chat_id, chatbot().db)
    if then_call is not None:
        callbacks()[then_call][1](query, then_call_with_data, update, context)


class AssignCallbacks:
    def __init__(self):
        self.callbacks = None
        self.on_receive = None

    def __call__(self, *args, **kwargs):
        return self.callbacks

    def provide(self, c) -> None:
        self.callbacks = c
        if self.on_receive is not None:
            self.on_receive(c)


callbacks = AssignCallbacks()
chatbot = GetChatbot()
Callback = chatbot, undo_callback_chat_callback, callbacks
