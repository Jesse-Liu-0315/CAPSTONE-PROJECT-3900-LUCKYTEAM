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

def wishlistDisplay(token):
    """
    Display the wish list of the user who is logged in
    :param token: the token of the user who is logged in
    :return: a list of movies which are in the wish list

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
    # get the user's information
    sql = "SELECT * FROM movie_wishlist_tbl"
    store = list(db.execute_query(sql))
    wishList = []
    for user in store:
        if user['user_id'] == auth_user_id:
            sql = "select * from movie_tbl where movie_id = ('%s')" %(user['movie_id'])
            data = list(db.execute_query(sql))
            wishList.append(data[0])
    # get the number of reviews
    wishList = movie.movie_num_review(wishList, 'review_num')
    return {'wishlist': wishList}

def wishlistAdd(token, movie_id):
    """
    Add a movie to the wish list in movie detail page
    :param token: the token of the user
    :param movie_id: the id of the movie
    :return: {}
    
    pre-condition: the movie id is valid
    error: InputError - token is invalid
    error: InputError - the movie has been added to the wish list
    """
    # check whether this token is valid
    sql = "SELECT * FROM token_tbl"
    store = list(db.execute_query(sql))
    check_valid_token(token, store)
    # decode the token, get the user's id
    input_dict = decode_jwt(token)
    auth_user_id = input_dict['u_id']
    # check whether the movie has been added to the wish list
    sql = "SELECT * FROM movie_wishlist_tbl"
    store = list(db.execute_query(sql))
    for user in store:
        if user['user_id'] == auth_user_id and user['movie_id'] == movie_id:
            raise InputError(description="The movie has been added to the wish list")
    # add the movie to the wish list
    sql = "INSERT INTO movie_wishlist_tbl (user_id, movie_id) VALUES ('%s', '%s')" %(auth_user_id, movie_id)
    db.execute_query(sql)
    return {}

def wishlistRemove(token, movie_id):
    """
    Remove a movie from the wish list in wishlist page
    :param token: the token of the user
    :param movie_id: the id of the movie
    :return: {}
    
    pre-condition: the movie id is valid
    error: InputError - token is invalid
    error: InputError - the movie has not been added to the wish list
    """
    # check whether this token is valid
    sql = "SELECT * FROM token_tbl"
    store = list(db.execute_query(sql))
    check_valid_token(token, store)
    # decode the token, get the user's id
    input_dict = decode_jwt(token)
    auth_user_id = input_dict['u_id']
    # check whether the movie has been added to the wish list
    sql = "SELECT * FROM movie_wishlist_tbl"
    store = list(db.execute_query(sql))
    for user in store:
        if user['user_id'] == auth_user_id and user['movie_id'] == movie_id:
            sql = "DELETE FROM movie_wishlist_tbl WHERE user_id = ('%s') AND movie_id = ('%s')" %(auth_user_id, movie_id)
            db.execute_query(sql)
            return {}
    raise InputError(description="The movie has not been added to the wish list")

def wishlistOther(user_id):
    """
    Display the wish list of the other user
    :param user_id: the id of the other user
    :return: a list of movies which are in the wish list
    
    pre-condition: the user id is valid"""
    sql = "SELECT * FROM movie_wishlist_tbl where user_id = ('%s')" %(user_id)
    store = list(db.execute_query(sql))
    wishList = []
    for user in store:
        sql = "select * from movie_tbl where movie_id = ('%s')" %(user['movie_id'])
        data = list(db.execute_query(sql))
        wishList.append(data[0])
    # get the number of reviews
    wishList = movie.movie_num_review(wishList, 'review_num')
    return {'wishlist': wishList}