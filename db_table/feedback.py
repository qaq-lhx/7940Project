from typing import List, Tuple, Optional


def get_comments_count(movie_id: int, db) -> int:
    cursor = db.cursor()
    cursor.execute("""select count(*) from Feedback where movieID = %s;""", (movie_id,))
    results = cursor.fetchall()
    cursor.close()
    if len(results) > 0:
        return results[0][0]
    else:
        return 0


def get_comments(movie_id: int, db) -> List[Tuple[int, int, str]]:
    cursor = db.cursor()
    cursor.execute("""select feedbackID, movieID, comment from Feedback where movieID = %s;""", (movie_id,))
    results = cursor.fetchall()
    cursor.close()
    return results


def get_comment_content(feedback_id: int, db) -> Optional[str]:
    cursor = db.cursor()
    cursor.execute("""select comment from Feedback where feedbackID = %s limit 1;""", (feedback_id,))
    results = cursor.fetchall()
    cursor.close()
    if len(results) > 0:
        return results[0][0]
    else:
        return None


def add_comment(feedback_id, movie_id, comment, db):
    cursor = db.cursor()
    cursor.execute("""insert into Feedback (feedbackID,movieID, comment) values (%s, %s, %s);""",
                   (feedback_id, movie_id, comment))
    cursor.close()
    db.commit()
