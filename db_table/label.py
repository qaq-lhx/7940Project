#this file do operation to table Label
def get_labels_from_db(movie_id,db):
    cursorObject = db.cursor()
    cursorObject.execute( "SELECT label FROM Label WHERE movieID=%s ORDER BY frequency LIMIT 13", (movie_id,))
    result = cursorObject.fetchall()
    cursorObject.close()
    return result


def add_label_to_db(movie_id,label,db):
    cursorObject = db.cursor()
    cursorObject.execute( "SELECT frequency FROM Label WHERE movieID=%s and label=%s ", (movie_id,label))
    result = cursorObject.fetchall()
    if len(result) == 0:
        cursorObject.execute("""INSERT INTO Label (movieID,label,frequency) VALUES ( %s , %s , %s )""",
                             (movie_id, label, 1))
    else:
        frequency = int(result[0][0])+1
        cursorObject.execute( """UPDATE Label SET frequency=%s WHERE movieID=%s and label=%s""",(frequency,movie_id,label))
    cursorObject.close()
    db.commit()
