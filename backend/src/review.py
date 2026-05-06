import sys
import os
import re
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from other import *
from error import InputError
#from backend.common import mysql_operate
from common import mysql_operate
from flask import jsonify
from datetime import datetime
from common.mysql_pool import db


def add_review(movie_id, token, content, review_rating, time):
    """
    add a review to a movie
    :param movie_id: the id of the movie
    :param token: the token of the user
    :param content: the content of the review
    :param review_rating: the rating of the review
    :param time: the time of the review
    :return: {}
    
    pre-condition: the user has logged in
    pre-condition: the movie_id is valid and the movie has been added to the database
    error: InputError - token is invalid
    
    """
    sql = "SELECT * FROM token_tbl"
    store = list(db.execute_query(sql))
    check_valid_token(token, store)
    # decode the token, get the user's id
    input_dict = decode_jwt(token)
    user_id = input_dict['u_id']
    # add the review to the database
    sql = "INSERT INTO movie_review_tbl (movie_id, user_id, content, review_date, review_like, review_dislike, rating_point) VALUES ('{}', '{}', '{}', '{}', 0, 0, '{}')".format(movie_id, user_id, content, time, review_rating)
    db.execute_query(sql)
    sql = "update movie_tbl set movie_rating = (select avg(rating_point) from movie_review_tbl where movie_id = '{}') where movie_id = '{}'".format(movie_id, movie_id)
    db.execute_query(sql)
    # get review_id
    sql = "SELECT * FROM movie_review_tbl"
    store = list(db.execute_query(sql))
    reviewID = store[-1]['review_id']
    return {'reviewID' : reviewID}

def like_review(movie_id, review_id):
    """
    like a review
    :param movie_id: the id of the movie
    :param review_id: the id of the review
    :return: {}
    
    """
    sql = "SELECT * FROM movie_review_tbl"
    store = list(db.execute_query(sql))
    for review in store:
        # find the movie and review
        if review['movie_id'] == movie_id and review['review_id'] == review_id:
            review['review_like'] += 1
            sql = "UPDATE movie_review_tbl SET review_like = '{}' WHERE review_id = '{}'".format(review['review_like'], review_id)
            db.execute_query(sql)
            return {}
    raise InputError(description="The review does not exist")

def dislike_review(movie_id, review_id):
    """
    dislike a review
    :param movie_id: the id of the movie
    :param review_id: the id of the review
    :return: {}
    
    """
    sql = "SELECT * FROM movie_review_tbl"
    store = list(db.execute_query(sql))
    for review in store:
        # find the movie and review
        if review['movie_id'] == movie_id and review['review_id'] == review_id:
            review['review_dislike'] += 1
            sql = "UPDATE movie_review_tbl SET review_dislike = '{}' WHERE review_id = '{}'".format(review['review_dislike'], review_id)
            db.execute_query(sql)
            return {}
    raise InputError(description="The review does not exist")

def delete_review(movie_id, review_id, token):
    """
    delete a review
    :param movie_id: the id of the movie
    :param review_id: the id of the review
    :param token: the token of the user
    :return: {}
    
    pre-condition: the user has logged in
    pre-condition: the movie_id is valid and the movie has been added to the database
    pre-condition: the review_id is valid and the review has been added to the database
    pre-condition: the review_id is exactly the review has that the user wants to delete
    
    error: InputError - token is invalid
    error: InputError - the user is not the author of the review and is not an admin
    """
    sql = "SELECT * FROM token_tbl"
    store = list(db.execute_query(sql))
    check_valid_token(token, store)
    # decode the token, get the user's id
    input_dict = decode_jwt(token)
    user_id = input_dict['u_id']
    sql = "SELECT * FROM movie_review_tbl"
    store = list(db.execute_query(sql))
    for review in store:
        # for normal user, check if the user is the author of the review
        if review['movie_id'] == movie_id and review['review_id'] == review_id and review['user_id'] == user_id:
            sql = "DELETE FROM movie_review_tbl WHERE review_id = '{}'".format(review_id)
            db.execute_query(sql)
            # update the movie's rating
            sql = "update movie_tbl set movie_rating = (select avg(rating_point) from movie_review_tbl where movie_id = '{}') where movie_id = '{}'".format(movie_id, movie_id)
            db.execute_query(sql)
            # avoid the case that the movie has no review
            sql = "SELECT * FROM movie_tbl WHERE movie_id = '{}'".format(movie_id)
            store = list(db.execute_query(sql))
            if store[0]['movie_rating'] == None:
                sql = "update movie_tbl set movie_rating = 0 where movie_id = '{}'".format(movie_id)
                db.execute_query(sql)
            return {}
        else:
            # for admin, check if the user is an admin
            sql = "SELECT * FROM user_tbl where user_id = '{}'".format(user_id)
            store = list(db.execute_query(sql))
            if store[0]['user_permission'] == "admin":
                sql = "DELETE FROM movie_review_tbl WHERE review_id = '{}'".format(review_id)
                db.execute_query(sql)
                # update the movie's rating
                sql = "update movie_tbl set movie_rating = (select avg(rating_point) from movie_review_tbl where movie_id = '{}') where movie_id = '{}'".format(movie_id, movie_id)
                db.execute_query(sql)
                # avoid the case that the movie has no review
                sql = "SELECT * FROM movie_tbl WHERE movie_id = '{}'".format(movie_id)
                store = list(db.execute_query(sql))
                if store[0]['movie_rating'] == None:
                    sql = "update movie_tbl set movie_rating = 0 where movie_id = '{}'".format(movie_id)
                    db.execute_query(sql)
                return {}
    raise InputError(description="The review does not exist or the user is not the author of the review and is not an admin")