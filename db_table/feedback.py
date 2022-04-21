# methods of database operation to table Feedback

def add_comment(feedback_id,movie_id, comment, db):
    cursor = db.cursor()
    cursor.execute("""insert into Feedback (feedbackID,movieID, comment) values (%s, %s, %s);""", (feedback_id,movie_id, comment))
    cursor.close()
    db.commit()
