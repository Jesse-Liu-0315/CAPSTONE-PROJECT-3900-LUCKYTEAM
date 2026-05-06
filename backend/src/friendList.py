import sys
import os
import re
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from other import *
from error import InputError
#from backend.common import mysql_operate
from common import mysql_operate
from common.mysql_pool import db

def friendlistDisplay(token):
    """
    Display the friend list of the user and sort by the lastest message time / unread_num
    :param token: the token of the user who is logged in
    :return: a list of users who are in the friend list
    
    pre-condition: the user has logged in
    pre-condition: the correct format of the message time in database
    error: InputError - token is invalid
    """
    # check whether this token is valid
    sql = "SELECT * FROM token_tbl"
    store = list(db.execute_query(sql))
    check_valid_token(token, store)
    # decode the token, get the user's id
    input_dict = decode_jwt(token)
    auth_user_id = input_dict['u_id']
    # get the friend list information of the user
    sql = "select * from user_friendship_tbl where user_id = ('%s')" %(auth_user_id)
    data = list(db.execute_query(sql))  # 用mysql_operate文件中的db的select_db方法进行查询
    friendlist = []
    for friend in data:
        sql = "select * from user_tbl where user_id = ('%s')" %(friend['friend_id'])
        friendlist.append(list(db.execute_query(sql))[0])
    # get the number of unread messages
    for friend in friendlist:
        sql = "select * from chat_tbl where receiver_id = ('%s') and sender_id = ('%s') and chat_unread = ('%s')" %(auth_user_id, friend['user_id'], 1)
        friend['unread_num'] = len(list(db.execute_query(sql)))
    # get the lastest message time
    for friend in friendlist:
        sql = "select * from chat_tbl where receiver_id = ('%s') and sender_id = ('%s') and chat_unread = ('%s')" %(auth_user_id, friend['user_id'], 0)
        data1 = list(db.execute_query(sql))
        sql = "select * from chat_tbl where receiver_id = ('%s') and sender_id = ('%s') and chat_unread = ('%s')" %(friend['user_id'], auth_user_id, 0)
        data2 = list(db.execute_query(sql))
        data = data1 + data2
        if len(data) == 0:
            friend['last_message_time'] = 0
        else:
            friend['last_message_time'] = data[-1]['chat_date']
    # sort by the lastest message and unread_num > 0
    sorted_list = sorted(friendlist, key=lambda x: x['last_message_time'], reverse=True)
    unread_list = [x for x in sorted_list if x['unread_num'] > 0]
    read_list = [x for x in sorted_list if x['unread_num'] == 0]
    final_list = unread_list + read_list
    return {
        'friendlist': final_list
    }

def friendlistAdd(token, friend_id, time):
    """
    Add a friend to the friend list
    :param token: the token of the user who is logged in
    :param friend_id: the id of the friend to be added
    :param time: the time when the friend is added
    :return: {}
    
    pre-condition: the user has logged in
    pre-condition: the correct format of time which can be sort
    error: InputError - token is invalid
    error: InputError - the user has been added to the friend list
    error: InputError - the user has been added to his/her black list
    error: InputError - the user has been added to the black list
    error: InputError - the user is yourself

    """
    # check whether this token is valid
    sql = "SELECT * FROM token_tbl"
    store = list(db.execute_query(sql))
    check_valid_token(token, store)
    # decode the token, get the user's id
    input_dict = decode_jwt(token)
    auth_user_id = input_dict['u_id']
    # check whether they are already friends
    sql = "SELECT * FROM user_friendship_tbl"
    store = list(db.execute_query(sql))
    for user in store:
        if user['user_id'] == auth_user_id and user['friend_id'] == friend_id:
            raise InputError(description="The user has been added to the friend list")
    # check whether the friend added me to his/her black list
    sql = "SELECT * FROM user_blacklist_tbl where user_id = ('%s') and black_id = ('%s')" %(friend_id, auth_user_id)
    store = list(db.execute_query(sql))
    if len(store) != 0:
        raise InputError(description="The user has been added to the black list")
    # check whether I added the friend to my black list
    sql = "SELECT * FROM user_blacklist_tbl where user_id = ('%s') and black_id = ('%s')" %(auth_user_id, friend_id)
    store = list(db.execute_query(sql))
    if len(store) != 0:
        raise InputError(description="The user has been added to the black list")
    # check whether the friend is myself
    if auth_user_id == friend_id:
        raise InputError(description="The user is yourself")
    # add the friend to the friend list
    sql = "INSERT INTO user_friendship_tbl (user_id, friend_id) VALUES ('%s', '%s')" %(auth_user_id, friend_id)
    db.execute_query(sql)
    sql = "INSERT INTO user_friendship_tbl (user_id, friend_id) VALUES ('%s', '%s')" %(friend_id, auth_user_id)
    db.execute_query(sql)
    # sned a hello message to the friend
    sql = "INSERT INTO chat_tbl (sender_id, receiver_id, chat_content, chat_date, chat_unread) VALUES ('%s', '%s', '%s', '%s', 1)" %(auth_user_id, friend_id, "Hello, I am your friend!", time)
    db.execute_query(sql)
    return {}

def friendlistRemove(token, friend_id):
    """
    Remove a friend from the friend list
    :param token: the token of the user who is logged in
    :param friend_id: the id of the friend to be removed
    :return: {}
    
    pre-condition: the user has logged in
    error: InputError - token is invalid
    error: InputError - the user is not in the friend list
    """
    # check whether this token is valid
    sql = "SELECT * FROM token_tbl"
    store = list(db.execute_query(sql))
    check_valid_token(token, store)
    # decode the token, get the user's id
    input_dict = decode_jwt(token)
    auth_user_id = input_dict['u_id']
    # check whether they are already friends
    sql = "SELECT * FROM user_friendship_tbl"
    store = list(db.execute_query(sql))
    for user in store:
        if user['user_id'] == auth_user_id and user['friend_id'] == friend_id:
            sql = "DELETE FROM user_friendship_tbl WHERE user_id = ('%s') and friend_id = ('%s')" %(auth_user_id, friend_id)
            db.execute_query(sql)
            sql = "DELETE FROM user_friendship_tbl WHERE user_id = ('%s') and friend_id = ('%s')" %(friend_id, auth_user_id)
            db.execute_query(sql)
            # delete chat history
            sql = "DELETE FROM chat_tbl WHERE sender_id = ('%s') and receiver_id = ('%s')" %(auth_user_id, friend_id)
            db.execute_query(sql)
            sql = "DELETE FROM chat_tbl WHERE sender_id = ('%s') and receiver_id = ('%s')" %(friend_id, auth_user_id)
            db.execute_query(sql)
            return {}
    raise InputError(description="The user is not in the friend list")