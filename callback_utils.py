import json

from db_table.callback_data import store


def callback(call: str, data, db):
    return str(store(json.dumps({
        'call': call,
        'data': data
    }), db))
