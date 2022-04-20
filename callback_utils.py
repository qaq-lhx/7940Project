import json
from typing import Optional, TYPE_CHECKING

from db_table.callback_data import store, store_chat

if TYPE_CHECKING:
    from telegram import Chat


def callback(call: str, data, db):
    return str(store(json.dumps({
        'call': call,
        'data': data
    }), db))


def callback_chat(chat: Optional['Chat'], call: str, data, db):
    if chat is not None:
        return str(store_chat(chat.id, json.dumps({
            'call': call,
            'data': data
        }), db))
    return None
