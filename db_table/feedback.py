#methods of database operation to table Feedback

def add_comment(movie_id,comment,db):
    cursorObject = db.cursor()
    cursorObject.execute("""INSERT INTO Feedback (movieID,comment,agree,disagree) VALUES ( %s , %s , %s , %s )""", (movie_id, comment, 0, 0))
    db.commit()