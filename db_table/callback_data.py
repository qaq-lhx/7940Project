def fetch_all_from_stored_procedure_selects(cursor):
    results = [stored_result.fetchall() for stored_result in cursor.stored_results()]
    return [result for sublist in results for result in sublist]


def store(callback_data: str, db):
    cursor = db.cursor()
    cursor.callproc('StoreCallbackData', (callback_data,))
    results = fetch_all_from_stored_procedure_selects(cursor)
    if len(results) > 0 and len(results[0]) > 0:
        return results[0][0]
    else:
        return None


def fetch(callback_data_id: int, db):
    cursor = db.cursor()
    cursor.callproc('FetchCallbackData', (callback_data_id,))
    results = fetch_all_from_stored_procedure_selects(cursor)
    if len(results) > 0 and len(results[0]) > 0:
        return results[0][0]
    else:
        return None


def store_chat(chat_id: int, callback_data: str, db):
    cursor = db.cursor()
    cursor.callproc('StoreCallbackDataWithChat', (chat_id, callback_data))
    results = fetch_all_from_stored_procedure_selects(cursor)
    if len(results) > 0 and len(results[0]) > 0:
        return results[0][0]
    else:
        return None


def fetch_chat(chat_id: int, db):
    cursor = db.cursor()
    cursor.callproc('FetchLatestCallbackDataByChat', (chat_id,))
    results = fetch_all_from_stored_procedure_selects(cursor)
    if len(results) > 0 and len(results[0]) > 0:
        return results[0][0]
    else:
        return None


def remove(callback_data_id: int, db):
    cursor = db.cursor()
    cursor.callproc('RemoveCallbackData', (callback_data_id,))


def remove_chat_all(chat_id: int, db):
    cursor = db.cursor()
    cursor.callproc('RemoveAllCallbackDataByChat', (chat_id,))
