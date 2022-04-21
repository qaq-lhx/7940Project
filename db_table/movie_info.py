from typing import List, Optional, Tuple


def get_movie_in_db(movie_id: int, db) -> Optional[Tuple[int, str, str, str, str, int, str]]:
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


def search_movie_in_db_by_exact_match(exact_match_keyword: str, excluded_ids: List[int], limit: int, db,
                                      prefix_matching: bool = False) -> List[Tuple[int, str, str]]:
    cursor = db.cursor()
    if prefix_matching:
        keyword = exact_match_keyword + '%'
    else:
        keyword = '%' + exact_match_keyword + '%'
    if len(excluded_ids) > 0:
        additional_condition = ' and id not in ({})'.format(', '.join(['%s'] * len(excluded_ids)))
        arguments = (keyword,) + tuple(excluded_ids) + (limit,)
    else:
        additional_condition = ''
        arguments = (keyword, limit)
    cursor.execute("""select id, name, year
            from MovieInfo
            where name like %s{}
            order by name
            limit %s;""".format(additional_condition), arguments)
    results = cursor.fetchall()
    cursor.close()
    return results


def search_movie_in_db_by_fulltext_match(keywords: List[str], excluded_ids: List[int], limit: int, db,
                                         exact_match_keyword: Optional[str] = None) -> List[Tuple[int, str, str]]:
    cursor = db.cursor()
    partial_match_keyword = ' '.join([keyword + '*' for keyword in keywords])
    if exact_match_keyword is None:
        exact_match_keyword = ' '.join(keywords)
    matcher = '({}) ("{}")'.format(partial_match_keyword, exact_match_keyword)
    if len(excluded_ids) > 0:
        additional_condition = 'where id not in ({})'.format(', '.join(['%s'] * len(excluded_ids)))
        arguments = (matcher,) + tuple(excluded_ids) + (limit,)
    else:
        additional_condition = ''
        arguments = (matcher, limit)
    # noinspection SqlAggregates
    cursor.execute("""select match(name, overview) against(%s in boolean mode) score, id, name, year
                    from MovieInfo
                    {}
                    having score > 0
                    order by score
                    desc limit %s;""".format(additional_condition), arguments)
    results = [result[1:] for result in cursor.fetchall()]
    cursor.close()
    return results


def search_movie_in_db(keywords: List[str], excluded_ids: List[int], limit: int, db) -> List[Tuple[int, str, str]]:
    exact_match_keyword = ' '.join(keywords)
    results = search_movie_in_db_by_exact_match(
        exact_match_keyword,
        excluded_ids,
        limit,
        db,
        prefix_matching=True
    )
    need_more = limit - len(results)
    if need_more > 0:
        results += search_movie_in_db_by_exact_match(
            exact_match_keyword,
            excluded_ids + [result[0] for result in results],
            need_more,
            db
        )
        need_more = limit - len(results)
        if need_more > 0:
            results += search_movie_in_db_by_fulltext_match(
                keywords,
                excluded_ids + [result[0] for result in results],
                need_more,
                db,
                exact_match_keyword=exact_match_keyword
            )
    return results


def recommend_movie_in_db(keywords, db):
    like_keyword = ' '.join(keywords)
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
