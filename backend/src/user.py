import sys
import os
import re
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from other import *
from error import InputError
from common import mysql_operate
from flask import jsonify
from common.mysql_pool import db

def user_addTag(id, token, tag):
    """
    Add a tag to a user only for admin
    :param id: the id of the user
    :param token: the token of the user who is logged in
    :param tag: the tag of the user
    :return: {}
    
    pre-condition: the user id is valid
    error: InputError - token is invalid
    error: InputError - the user is not admin
    """
    # check if the user is admin
    sql = "SELECT * FROM token_tbl"
    store = list(db.execute_query(sql))
    check_valid_token(token, store)
    # decode the token, get the user's id
    input_dict = decode_jwt(token)
    auth_user_id = input_dict['u_id']
    sql = "SELECT * FROM user_tbl WHERE user_id = ('%s')" %(auth_user_id)
    data = list(db.execute_query(sql))
    if data[0]['user_permission'] != 'admin':
        raise InputError(description="The user is not admin")
    # add tag
    sql = "UPDATE user_tbl SET user_tag = ('%s') WHERE user_id = ('%s')" %(tag, id)
    db.execute_query(sql)
    return {}

def user_detail(id, token):
    """
    Get the detail information of other user
    :param id: the id of the user
    :param token: the token of the user who is logged in
    :return: a dictionary of the user's detail information
    pre-condition: the user id is valid
    error: InputError - token is invalid
    """
    sql = "select * from user_tbl where user_id = ('%s')" %(id)
    data = list(db.execute_query(sql))  # 用mysql_operate文件中的db的select_db方法进行查询
    # 更新浏览量
    sql = "UPDATE user_tbl SET user_views = user_views + 1 WHERE user_id = '{}'".format(id)
    db.execute_query(sql)
    # get the number of friends
    sql = "SELECT * FROM user_friendship_tbl where user_id = ('%s')" %(id)
    store = list(db.execute_query(sql))
    numFriends = len(store)
    # get permission of the user
    # check if the user has added the user to blacklist and friends
    if token == '':
        return {
            'user': data[0],
            'blacklist': False,
            'friends': False,
            'numFriends': numFriends,
            'permission': False
        }
    else:
        sql = "SELECT * FROM token_tbl"
        store = list(db.execute_query(sql))
        check_valid_token(token, store)
        # decode the token, get the user's id
        input_dict = decode_jwt(token)
        auth_user_id = input_dict['u_id']
        # check if the user has added the user to blacklist
        blacklistres = False
        sql = "SELECT * FROM user_blacklist_tbl where user_id = ('%s') and black_id = ('%s')" %(auth_user_id, id)
        blacklist = list(db.execute_query(sql))
        if blacklist:
            blacklistres = True
        # check if the user has added the user to friends
        friendsres = False
        sql = "SELECT * FROM user_friendship_tbl where user_id = ('%s') and friend_id = ('%s')" %(auth_user_id, id)
        friends = list(db.execute_query(sql))
        if friends:
            friendsres = True
        # check if the user is admin
        permission = False
        sql = "SELECT * FROM user_tbl WHERE user_id = ('%s')" %(auth_user_id)
        data1 = list(db.execute_query(sql))
        if data1[0]['user_permission'] == 'admin':
            permission = True
        return {
            'user': data[0],
            'blacklist': blacklistres,
            'friends': friendsres,
            'numFriends': numFriends,
            'permission': permission
        }

def user_search(word, pages, token, sortBy):
    """
    Search the user by the word and sort by the sort method (for login user or not)
    :param word: the word to search
    :param pages: the page number
    :param token: the token of the user who is logged in
    :param sortBy: the sort method
    :return: a dictionary of the users' information
    error: InputError - token is invalid
    
    pre-condition: the sortBy is correct"""
    sql = "select * from user_tbl where user_name like ('%{}%')".format(word)
    data = list(db.execute_query(sql))
    # check if the user has added the user to blacklist and friends
    if token == '':
        # for log out user
        pages = pages - 1
        if sortBy == 'Name: A to Z':
            data = sorted(data, key=lambda x: x['user_name'])
        elif sortBy == 'Name: Z to A':
            data = sorted(data, key=lambda x: x['user_name'], reverse=True)
        elif sortBy == 'Views: Less to More':
            data = sorted(data, key=lambda x: x['user_views'])
        elif sortBy == 'Views: More to Less':
            data = sorted(data, key=lambda x: x['user_views'], reverse=True)
        return {
            'users': data[5 * pages: 5 * pages + 5],
            'numPages': len(data) // 5 + 1
        }
    else:
        # for log in user
        sql = "SELECT * FROM token_tbl"
        store = list(db.execute_query(sql))
        check_valid_token(token, store)
        # decode the token, get the user's id
        input_dict = decode_jwt(token)
        auth_user_id = input_dict['u_id']
        result = []
        # delete the user who has been added to blacklist
        for other in data:
            sql = "SELECT * FROM user_blacklist_tbl where user_id = ('%s') and black_id = ('%s')" %(auth_user_id, other['user_id'])
            blacklist = list(db.execute_query(sql))
            if blacklist:
                continue
            else:
                result.append(other)
        # check if the user has added the user to friends
        for other in result:
            sql = "SELECT * FROM user_friendship_tbl where user_id = ('%s') and friend_id = ('%s')" %(auth_user_id, other['user_id'])
            friends = list(db.execute_query(sql))
            if friends:
                other['friends'] = True
            else:
                other['friends'] = False
        pages = pages - 1
        if sortBy == 'Name: A to Z':
            data = sorted(data, key=lambda x: x['user_name'])
        elif sortBy == 'Name: Z to A':
            data = sorted(data, key=lambda x: x['user_name'], reverse=True)
        elif sortBy == 'Views: Less to More':
            data = sorted(data, key=lambda x: x['user_views'])
        elif sortBy == 'Views: More to Less':
            data = sorted(data, key=lambda x: x['user_views'], reverse=True)
        return {
            'users': result[5 * pages: 5 * pages + 5],
            'numPages': len(result) // 5 + 1
        }