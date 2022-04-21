#this file do some database operation about table rating


def insert_rating_in_db(movie_id,score,db):    
    cursorObject = db.cursor()
    cursorObject.execute( """INSERT INTO Rating (movieID,rating) VALUES ( %s , %s )""",(movie_id,score))
    db.commit()