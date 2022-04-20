def get_movie_in_db(movie_id, db):
    cursor = db.cursor()
    cursor.execute("""select id, name, imdbID, poster, genres, year, overview
        from MovieInfo
        where id = %s
        limit 1;""", (movie_id,))
    results = cursor.fetchall()
    if len(results) > 0:
        return results[0]
    else:
        return None


def search_movie_in_db(keywords, db):
    exact_match_keyword = ' '.join(keywords)
    limit = 10
    cursor = db.cursor()
    cursor.execute("""select id, name, year
        from MovieInfo
        where name like %s
        order by name
        limit %s;""", (exact_match_keyword + '%', limit))
    results = cursor.fetchall()
    need_more = limit - len(results)
    if need_more > 0:
        cursor.execute("""select id, name, year
                from MovieInfo
                where name like %s and id not in (%s)
                order by name
                limit %s;""", ('%' + exact_match_keyword + '%', [result[0] for result in results], need_more))
        results += cursor.fetchall()
    need_more = limit - len(results)
    if need_more > 0:
        partial_match_keyword = ' '.join([keyword + '*' for keyword in keywords])
        matcher = '({}) ("{}")'.format(partial_match_keyword, exact_match_keyword)
        cursor.execute("""select match(name, overview) against(%s in boolean mode) score, id, name, year
            from MovieInfo
            where id not in (%s)
            having score > 0
            order by score
            desc limit %s;""", (matcher, [result[0] for result in results], need_more))
        results += [result[1:] for result in cursor.fetchall()]
    return results
