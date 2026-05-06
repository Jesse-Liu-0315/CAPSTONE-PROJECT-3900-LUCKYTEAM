import sys
import os
import re
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from other import *
from error import InputError
#from backend.common import mysql_operate
from common import mysql_operate
from common.mysql_pool import db
import movie


def alreadyseenlistDisplay(token):
    """
    watchlist display page for self
    :param token: the token of the user
    :return: a list of movies that the user has added to watched lust

    pre-condition: the user has logged in
    error: InputError - token is invalid

    """
    # check whether this token is valid
    sql = "SELECT * FROM token_tbl"
    store = list(db.execute_query(sql))
    check_valid_token(token, store)
    # decode the token, get the user's id
    input_dict = decode_jwt(token)
    auth_user_id = input_dict['u_id']
    # get the user's watched list information
    sql = "SELECT * FROM movie_watchlist_tbl where user_id = ('%s')" %(auth_user_id)
    store = list(db.execute_query(sql))
    alreadyseenList = []
    for mo in store:
        sql = "select * from movie_tbl where movie_id = ('%s')" %(mo['movie_id'])
        data = list(db.execute_query(sql))
        alreadyseenList.append(data[0])
    # get the number of reviews for each movie
    alreadyseenList = movie.movie_num_review(alreadyseenList, 'review_num')
    return {'watchedlist' : alreadyseenList}

def alreadyseenlistAdd(token, movie_id):
    """
    add a movie to the watched list in movie detail page
    :param token: the token of the user
    :param movie_id: the id of the movie
    :return: {}

    pre-condition: the user has logged in
    pre-condition: the movie_id is vaiid and the movie has been added to the database
    error: InputError - token is invalid
    error: InputError - the movie has been added to the watched list
    """
    # check whether this token is valid
    sql = "SELECT * FROM token_tbl"
    store = list(db.execute_query(sql))
    check_valid_token(token, store)
    # decode the token, get the user's id
    input_dict = decode_jwt(token)
    auth_user_id = input_dict['u_id']
    # check whether the movie has been added to the wish list
    sql = "SELECT * FROM movie_watchlist_tbl where user_id = ('%s') and movie_id = ('%s')" %(auth_user_id, movie_id)
    store = list(db.execute_query(sql))
    if len(store) != 0:
        raise InputError(description="The movie has been added to the wish list")
    # add the movie to the wish list
    sql = "INSERT INTO movie_watchlist_tbl (user_id, movie_id) VALUES ('%s', '%s')" %(auth_user_id, movie_id)
    db.execute_query(sql)
    return {}

def alreadyseenlistRemove(token, movie_id):
    """
    remove a movie from the watched list in watchlist display page
    :param token: the token of the user
    :param movie_id: the id of the movie
    :return: {}

    pre-condition: the user has logged in
    error: InputError - token is invalid
    error: InputError - the movie has not been added to the watched list
    """
    # check whether this token is valid
    sql = "SELECT * FROM token_tbl"
    store = list(db.execute_query(sql))
    check_valid_token(token, store)
    # decode the token, get the user's id
    input_dict = decode_jwt(token)
    auth_user_id = input_dict['u_id']
    # check whether the movie has been added to the wish list
    sql = "SELECT * FROM movie_watchlist_tbl where user_id = ('%s') and movie_id = ('%s')" %(auth_user_id, movie_id)
    store = list(db.execute_query(sql))
    if len(store) != 0:
        sql = "DELETE FROM movie_watchlist_tbl WHERE user_id = ('%s') AND movie_id = ('%s')" %(auth_user_id, movie_id)
        db.execute_query(sql)
        return {}
    raise InputError(description="The movie has not been added to the wish list")

def alreadyseenlistOther(user_id):
    """
    get the watched list of other users in other user profile page
    :param user_id: the id of the user
    :return: a list of movies that the user has added to watched list

    pre-condition: the user_id is valid
    pre-condition: the movie_id is vaiid and the movie has been added to the database
    error: InputError - the user_id is invalid
    """
    # get the user's information
    sql = "SELECT * FROM movie_watchlist_tbl where user_id = ('%s')" %(user_id)
    store = list(db.execute_query(sql))
    alreadyseenList = []
    for mov in store:
        sql = "select * from movie_tbl where movie_id = ('%s')" %(mov['movie_id'])
        data = list(db.execute_query(sql))
        alreadyseenList.append(data[0])
    # get the number of reviews
    alreadyseenList = movie.movie_num_review(alreadyseenList, 'review_num')
    return {'watchedlist': alreadyseenList}