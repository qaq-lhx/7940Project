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
    cursor = db.cursor()
    cursor.execute("""insert into Rating (movieID, rating) values (%s, %s);""", (movie_id, score))
    cursor.close()
    db.commit()
