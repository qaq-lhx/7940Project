import json
from typing import Optional, TYPE_CHECKING

from db_table.callback_data import store, store_chat

if TYPE_CHECKING:
    from telegram import Chat


def callback(call: str, data, db) -> str:
    return str(store(json.dumps({
        'call': call,
        'data': data
    }), db))


def callback_chat(chat: Optional['Chat'], call: str, data, db) -> int:
    if chat is not None:
        return store_chat(chat.id, json.dumps({
            'call': call,
            'data': data
        }), db)
    return -1
