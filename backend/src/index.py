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

def index():
    """
    Index page
    :return: {
        'MostReviewed': movie list has most reviews,
        'TopRated': movie list has highest rating,
        'MostRecent': movie list release date is most recent
        }
    
    """
    # return movie has most reviews
    sql = "select * from movie_tbl"
    movie = list(db.execute_query(sql))
    # return movie has highest rating
    sql = "select * from movie_tbl order by movie_rating desc"
    movie2 = list(db.execute_query(sql))
    # return movie release date is most recent
    sql = "select * from movie_tbl order by movie_release_date desc"
    movie3 = list(db.execute_query(sql))
    if movie == []:
        movie = movie2
    # get movie review number
    for mov in movie:
        mov = movi.movie_num_review_single(mov)
    movie = sorted(movie, key=lambda x: x['numOfReviews'], reverse=True)
    for mov in movie2:
        mov = movi.movie_num_review_single(mov)
    for mov in movie3:
        mov = movi.movie_num_review_single(mov)
    return {
        'MostReviewed': movie[:5],
        'TopRated': movie2[:5],
        'MostRecent': movie3[:5]
    }
