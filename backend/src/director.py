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

def director_detail(id):
    """
    get director detail and update views
    :param id: director id
    :return: {
        'director': director info,
        'movie': movies that this director have been directed by this director
    }

    """
    # get director info
    sql = "select * from director_tbl where director_id = ('%s')" %(id)
    data = list(db.execute_query(sql))  # 用mysql_operate文件中的db的select_db方法进行查询
    # get the movies that the director have been directed by this director
    sql = "select * from direct_in_tbl where director_id = ('%s')" %(id)
    movie = list(db.execute_query(sql))
    movielist = []
    for mov in movie:
        sql = "select * from movie_tbl where movie_id = ('%s')" %(mov['movie_id'])
        mo = list(db.execute_query(sql))[0]
        movielist.append(mo)
    # get movie review number
    movielist = movi.movie_num_review(movielist, 'numOfReviews')
    # update views
    sql = "UPDATE director_tbl SET director_views = director_views + 1 WHERE director_id = ('%s')" %(id)
    db.execute_query(sql)
    
    return {
        'director': data[0],
        'movie': movielist
    }

def director_search(word, pages, sortBy):
    """
    search director by name or movie name
    :param word: search word
    :param pages: page number
    :param sortBy: sort by name or performance or views or age
    :return: {
        'director': director list
        'numOfResults': number of results page
    }
    
    """
    # search director by his/her name
    sql = "select * from director_tbl where director_name like '%{}%'".format(word)
    director = list(db.execute_query(sql))  # 用mysql_operate文件中的db的select_db方法进行查询
    # search director by movie name that he/she has been directed in
    sql = "select * from direct_in_tbl where movie_id in (select movie_id from movie_tbl where movie_name like '%{}%')".format(word)
    dir_in = list(db.execute_query(sql))
    for dir in dir_in:
        sql = "select * from director_tbl where director_id = ('%s')" %(dir['director_id'])
        director.append(list(db.execute_query(sql))[0])
    # remove duplicate
    new_list = []
    for item in director:
        if item not in new_list:
            new_list.append(item)
    director = new_list
    # add number of performances
    for c in director:
        sql = "select * from direct_in_tbl where director_id = ('%s')" %(c['director_id'])
        c['numOfPerformances'] = len(list(db.execute_query(sql)))
    pages = pages - 1
    # deal with the dirty data
    for c in director:
        if ',' not in c['director_birth']:
            c['director_birth'] = c['director_birth'] + ',0'
        if c['director_name'] == 'NULL':
            c['director_name'] = 'Unknown'
    if sortBy == 'Name: Z to A':
        director = sorted(director, key=lambda x: x['director_name'], reverse=True)
    elif sortBy == 'Name: A to Z':
        director = sorted(director, key=lambda x: x['director_name'], reverse=False)
    elif sortBy == 'Performances: More to Less':
        director = sorted(director, key=lambda x: x['numOfPerformances'], reverse=True)
    elif sortBy == 'Performances: Less to More':
        director = sorted(director, key=lambda x: x['numOfPerformances'], reverse=False)
    elif sortBy == 'Views: More to Less':
        director = sorted(director, key=lambda x: x['director_views'], reverse=True)
    elif sortBy == 'Views: Less to More':
        director = sorted(director, key=lambda x: x['director_views'], reverse=False)
    elif sortBy == 'Age: Old to Young':
        director = sorted(director, key=lambda x: x['director_birth'].split(',')[1], reverse=True)
    elif sortBy == 'Age: Young to Old':
        director = sorted(director, key=lambda x: x['director_birth'].split(',')[1],reverse=False)
    return {
        'directors': director[5 * pages: 5 * pages + 5],
        'numPages': len(director) // 5 + 1
    }
