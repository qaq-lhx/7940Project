from typing import List, Dict


def get_movie_average_ratings(movie_ids: List[int], db) -> Dict[int, float]:
    cursor = db.cursor()
    cursor.execute("""select movieID, avg(rating)
        from Rating
        where movieID in ({})
        group by movieID;""".format(', '.join(['%s'] * len(movie_ids))), tuple(movie_ids))
    results = cursor.fetchall()
    cursor.close()
    return {movie_id: float(average_rating) for movie_id, average_rating in results}


def insert_rating_in_db(movie_id, score, db):
    cursorObject = db.cursor()
    cursorObject.execute("""INSERT INTO Rating (movieID,rating) VALUES ( %s , %s )""", (movie_id, score))
    db.commit()
