from typing import Optional


def get_likes_count(feedback_id: int, db) -> int:
    cursor = db.cursor()
    cursor.execute("""select count(*) from FeedbackReaction where feedbackID = %s and reaction = 0b1;""",
                   (feedback_id,))
    results = cursor.fetchall()
    cursor.close()
    if len(results) > 0:
        return results[0][0]
    else:
        return 0


def get_dislikes_count(feedback_id: int, db) -> int:
    cursor = db.cursor()
    cursor.execute("""select count(*) from FeedbackReaction where feedbackID = %s and reaction = 0b0;""",
                   (feedback_id,))
    results = cursor.fetchall()
    cursor.close()
    if len(results) > 0:
        return results[0][0]
    else:
        return 0


def get_reaction(feedback_id: int, user_id: int, db) -> Optional[bool]:
    cursor = db.cursor()
    cursor.execute("""select reaction from FeedbackReaction where feedbackID = %s and userID = %s limit 1;""",
                   (feedback_id, user_id))
    results = cursor.fetchall()
    cursor.close()
    db.commit()
    if len(results) > 0:
        return bool(results[0][0])
    else:
        return None


def add_reaction(feedback_id: int, user_id: int, reaction: bool, db):
    cursor = db.cursor()
    cursor.execute("""insert into FeedbackReaction(feedbackID, userID, reaction) values (%s, %s, %s);""",
                   (feedback_id, user_id, reaction))
    cursor.close()
    db.commit()


def remove_reaction(feedback_id: int, user_id: int, db):
    cursor = db.cursor()
    cursor.execute("""delete from FeedbackReaction where feedbackID = %s and userID = %s;""", (feedback_id, user_id))
    cursor.close()
    db.commit()


def update_reaction(feedback_id: int, user_id: int, reaction: Optional[bool], db):
    remove_reaction(feedback_id, user_id, db)
    if reaction is not None:
        add_reaction(feedback_id, user_id, reaction, db)
