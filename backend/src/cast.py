import sys
import os
import re
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from other import *
from error import InputError
from common import mysql_operate
from flask import jsonify
from common.mysql_pool import db
import movie as movi

def cast_detail(id):
    """
    get cast detail and update views
    :param id: cast id
    :return: {
        'cast': cast info,
        'movie': movies that this cast have been cast in
    }
    """
    # get cast info
    sql = "select * from star_tbl where star_id = ('%s')" %(id)
    data = list(db.execute_query(sql))  
    # Get the movies that have been cast in.
    sql = "select * from star_in_tbl where star_id = ('%s')" %(id)
    movie = list(db.execute_query(sql))
    movielist = []
    for mov in movie:
        sql = "select * from movie_tbl where movie_id = ('%s')" %(mov['movie_id'])
        mo = list(db.execute_query(sql))[0]
        movielist.append(mo)
    # get movie review number
    movielist = movi.movie_num_review(movielist, 'numOfReviews')
    # update views
    sql = "UPDATE star_tbl SET star_views = star_views + 1 WHERE star_id = ('%s')" %(id)
    db.execute_query(sql)
    
    return {
        'cast': data[0],
        'movie': movielist
    }

def cast_search(word, pages, sortBy):
    """
    search cast by name or movie name
    :param word: search word
    :param pages: page number
    :param sortBy: sort by name or performance or views or age
    :return: {
        'cast': cast list
        'numOfResults': number of results
    }
    
    """
    # search cast by his/her name
    sql = "select * from star_tbl where star_name like '%{}%'".format(word)
    cast = list(db.execute_query(sql))  
    # search cast by movie name that he/she has been cast in
    sql = "select * from star_in_tbl where movie_id in (select movie_id from movie_tbl where movie_name like '%{}%')".format(word)
    dir_in = list(db.execute_query(sql))
    for dir in dir_in:
        sql = "select * from star_tbl where star_id = ('%s')" %(dir['star_id'])
        cast.append(list(db.execute_query(sql))[0])
    # remove duplicate
    new_list = []
    for item in cast:
        if item not in new_list:
            new_list.append(item)
    cast = new_list
    # add number of performances
    for c in cast:
        sql = "select * from star_in_tbl where star_id = ('%s')" %(c['star_id'])
        c['numOfPerformances'] = len(list(db.execute_query(sql)))
    pages = pages - 1
    # deal with dirty data
    for c in cast:
        if ',' not in c['star_birth']:
            c['star_birth'] = c['star_birth'] + ',0'
        if c['star_name'] == 'NULL':
            c['star_name'] = 'Unknown'
    if sortBy == 'Name: A to Z':
        cast = sorted(cast, key=lambda x: x['star_name'])
    elif sortBy == 'Name: Z to A':
        cast = sorted(cast, key=lambda x: x['star_name'], reverse=True)
    elif sortBy == 'Performances: Less to More':
        cast = sorted(cast, key=lambda x: x['numOfPerformances'])
    elif sortBy == 'Performances: More to Less':
        cast = sorted(cast, key=lambda x: x['numOfPerformances'], reverse=True)
    elif sortBy == 'Views: Less to More':
        cast = sorted(cast, key=lambda x: x['star_views'])
    elif sortBy == 'Views: More to Less':
        cast = sorted(cast, key=lambda x: x['star_views'], reverse=True)
    elif sortBy == 'Age: Old to Young':
        cast = sorted(cast, key=lambda x: x['star_birth'].split(',')[1])
    elif sortBy == 'Age: Young to Old':
        cast = sorted(cast, key=lambda x: x['star_birth'].split(',')[1], reverse=True)
    return {
        'casts': cast[5 * pages: 5 * pages + 5],
        'numPages': len(cast) // 5 + 1
    }