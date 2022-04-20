import json

from db_table.callback_data import store, store_chat


def callback(call: str, data, db):
    return str(store(json.dumps({
        'call': call,
        'data': data
    }), db))


def callback_chat(chat_id: int, call: str, data, db):
    return str(store_chat(chat_id, json.dumps({
        'call': call,
        'data': data
    }), db))
