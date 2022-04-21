def get_movie_in_db(movie_id, db):
    cursor = db.cursor()
    cursor.execute("""select id, name, imdbID, poster, genres, year, overview
        from MovieInfo
        where id = %s
        limit 1;""", (movie_id,))
    results = cursor.fetchall()
    cursor.close()
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
        if len(results) > 0:
            exclude_ids = ' and id not in ({})'.format(', '.join(['%s'] * len(results)))
            arguments = ('%' + exact_match_keyword + '%',) + tuple([result[0] for result in results]) + (need_more,)
        else:
            exclude_ids = ''
            arguments = ('%' + exact_match_keyword + '%', need_more)
        cursor.execute("""select id, name, year
                from MovieInfo
                where name like %s{}
                order by name
                limit %s;""".format(exclude_ids), arguments)
        results += cursor.fetchall()
    need_more = limit - len(results)
    if need_more > 0:
        partial_match_keyword = ' '.join([keyword + '*' for keyword in keywords])
        matcher = '({}) ("{}")'.format(partial_match_keyword, exact_match_keyword)
        if len(results) > 0:
            exclude_ids = 'where id not in ({})'.format(', '.join(['%s'] * len(results)))
            arguments = (matcher,) + tuple([result[0] for result in results]) + (need_more,)
        else:
            exclude_ids = ''
            arguments = (matcher, need_more)
        cursor.execute("""select match(name, overview) against(%s in boolean mode) score, id, name, year
            from MovieInfo
            {}
            having score > 0
            order by score
            desc limit %s;""".format(exclude_ids), arguments)
        results += [result[1:] for result in cursor.fetchall()]
    cursor.close()
    return results

def recommend_movie_in_db(keywords, db):
    like_keyword =' '.join(keywords)
    limit = 5
    cursor = db.cursor()
    cursor.execute("""SELECT MovieInfo.id, MovieInfo.name, MovieInfo.year,round(AVG(Rating.rating),1)
        FROM MovieInfo INNER JOIN Rating ON MovieInfo.id=Rating.movieID 
        WHERE MovieInfo.genres LIKE %s 
        GROUP BY MovieInfo.name, MovieInfo.id 
        order by AVG(Rating.rating) desc
        limit %s;""", ('%' + like_keyword + '%', limit))
    results = cursor.fetchall()
    
    cursor.close()
    return results

def get_movie_AVGrating_in_db(movie_id, db):
    cursor = db.cursor()
    cursor.execute("""SELECT movieID, round(AVG(rating),1)
        FROM Rating 
        WHERE movieID = %s 
        group by movieID 
        limit 1;""", (movie_id,))
    results = cursor.fetchall()
    cursor.close()
    if len(results) > 0:
        return results[0]
    else:
        return None