from typing import Optional, Tuple

from db_table import fetch_all_from_stored_procedure_selects


def store(callback_data: str, db) -> Optional[int]:
    cursor = db.cursor()
    cursor.callproc('StoreCallbackData', (callback_data,))
    results = fetch_all_from_stored_procedure_selects(cursor)
    cursor.close()
    db.commit()
    if len(results) > 0 and len(results[0]) > 0:
        return results[0][0]
    else:
        return None


def fetch(callback_data_id: int, db) -> Optional[str]:
    cursor = db.cursor()
    cursor.callproc('FetchCallbackData', (callback_data_id,))
    results = fetch_all_from_stored_procedure_selects(cursor)
    cursor.close()
    if len(results) > 0 and len(results[0]) > 0:
        return results[0][0]
    else:
        return None


def store_chat(chat_id: int, callback_data: str, db) -> Optional[int]:
    cursor = db.cursor()
    cursor.callproc('StoreCallbackDataWithChat', (chat_id, callback_data))
    results = fetch_all_from_stored_procedure_selects(cursor)
    cursor.close()
    db.commit()
    if len(results) > 0 and len(results[0]) > 0:
        return results[0][0]
    else:
        return None


def fetch_chat(chat_id: int, db) -> Optional[Tuple[int, str]]:
    cursor = db.cursor()
    cursor.callproc('FetchLatestCallbackDataWithIdByChat', (chat_id,))
    results = fetch_all_from_stored_procedure_selects(cursor)
    cursor.close()
    if len(results) > 0 and len(results[0]) > 0:
        return results[0][0], results[0][1]
    else:
        return None


def remove(callback_data_id: int, db):
    cursor = db.cursor()
    cursor.callproc('RemoveCallbackData', (callback_data_id,))
    cursor.close()
    db.commit()


def remove_chat_all(chat_id: int, db):
    cursor = db.cursor()
    cursor.callproc('RemoveAllCallbackDataByChat', (chat_id,))
    cursor.close()
    db.commit()
