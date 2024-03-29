import json
from typing import Optional, TYPE_CHECKING

from db_table.callback_data import store, store_chat, remove, remove_chat_all

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


def undo_callback_chat(callback_chat_instance: int, db):
    remove(callback_chat_instance, db)


def undo_callback_chat_all(chat: Optional['Chat'], db):
    if chat is not None:
        undo_callback_chat_all_by_chat_id(chat.id, db)


def undo_callback_chat_all_by_chat_id(chat_id: int, db):
    remove_chat_all(chat_id, db)
