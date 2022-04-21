# methods of database operation to table Feedback

def add_comment(movie_id, comment, db):
    cursor = db.cursor()
    cursor.execute("""insert into Feedback (movieID, comment) values (%s, %s);""", (movie_id, comment))
    cursor.close()
    db.commit()
