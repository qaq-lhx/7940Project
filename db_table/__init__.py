def fetch_all_from_stored_procedure_selects(cursor):
    results = [stored_result.fetchall() for stored_result in cursor.stored_results()]
    return [result for sublist in results for result in sublist]
