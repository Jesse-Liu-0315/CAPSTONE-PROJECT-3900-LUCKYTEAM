import sys
import os
import re
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from other import *
from error import InputError
#from backend.common import mysql_operate
from common import mysql_operate
from common.mysql_pool import db


def blacklistDisplay(token):
    """
    Display the black list of the user who is logged in
    :param token: the token of the user who is logged in
    :return: a list of users who are in the black list

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
    # get the user's black list information
    sql = "SELECT * FROM user_blacklist_tbl where user_id = ('%s')" %(auth_user_id)
    store = list(db.execute_query(sql))
    blackList = []
    for user in store:
        sql = "select * from user_tbl where user_id = ('%s')" %(user['black_id'])
        data = list(db.execute_query(sql))

        # get the number of friends of the black user
        sql = "select * from user_friendship_tbl where user_id = ('%s')" %(user['black_id'])
        data[0]['friend_num'] = len(list(db.execute_query(sql)))

        blackList.append(data[0])
    return {'blacklist': blackList}

def blacklistAdd(token, black_id):
    """
    Add a user to the black list
    :param token: the token of the user who is logged in
    :param black_id: the id of the user who would be added to the black list
    :return: {}

    pre-condition: the user has logged in
    error: InputError - token is invalid
    error: InputError - the user has been added to the black list
    error: InputError - the user is in the friend list

    """
    # check whether this token is valid
    sql = "SELECT * FROM token_tbl"
    store = list(db.execute_query(sql))
    check_valid_token(token, store)
    # decode the token, get the user's id
    input_dict = decode_jwt(token)
    auth_user_id = input_dict['u_id']
    # check whether the user has been added to the black list
    sql = "SELECT * FROM user_blacklist_tbl where user_id = ('%s') and black_id = ('%s')" %(auth_user_id, black_id)
    store = list(db.execute_query(sql))
    if len(store) != 0:
        raise InputError(description="The user has been added to the black list")
    # check whether the user is in the friend list
    sql = "SELECT * FROM user_friendship_tbl where user_id = ('%s') and friend_id = ('%s')" %(auth_user_id, black_id)
    store = list(db.execute_query(sql))
    if len(store) != 0:
        raise InputError(description="The user is in the friend list")
    # check whether the user and black_id are the same
    if auth_user_id == black_id:
        raise InputError(description="The user and black_id are the same")
    # add the user to the black list
    sql = "INSERT INTO user_blacklist_tbl (user_id, black_id) VALUES ('%s', '%s')" %(auth_user_id, black_id)
    db.execute_query(sql)
    return {}

def alreadyseenlistRemove(token, black_id):
    """
    Remove a user from the black list
    :param token: the token of the user who is logged in
    :param black_id: the id of the user who would be removed from the black list
    :return: {}
        
    pre-condition: the user has logged in
    error: InputError - token is invalid
    error: InputError - the user has not been added to the black list

    """
    # check whether this token is valid
    sql = "SELECT * FROM token_tbl"
    store = list(db.execute_query(sql))
    check_valid_token(token, store)
    # decode the token, get the user's id
    input_dict = decode_jwt(token)
    auth_user_id = input_dict['u_id']
    # check whether the user has been added to the black list
    sql = "SELECT * FROM user_blacklist_tbl where user_id = ('%s') and black_id = ('%s')" %(auth_user_id, black_id)
    store = list(db.execute_query(sql))
    if len(store) != 0:
        sql = "DELETE FROM user_blacklist_tbl WHERE user_id = ('%s') AND black_id = ('%s')" %(auth_user_id, black_id)
        db.execute_query(sql)
        return {}
    raise InputError(description="The user has not been added to the black list")