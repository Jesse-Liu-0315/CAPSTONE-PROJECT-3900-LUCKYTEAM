import sys
import os
import re
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from other import *
from error import InputError
from common import mysql_operate
from flask import jsonify
from common.mysql_pool import db

def messageList(token, friendID):
    """
    get the message list between two users and mark all the messages as read
    :param token: the token of the user who is logged in
    :param friendID: the id of the user who is the friend of the user who is logged in
    :return: a list of messages between two users with the information of the sender and the receiver

    pre-condition: the user has logged in
    error: InputError - token is invalid
    error: InputError - the user is not your friend
    error: InputError - the user has been added to the black list

    """
    # check vaild token
    sql = "SELECT * FROM token_tbl"
    store = list(db.execute_query(sql))
    check_valid_token(token, store)
    # decode the token, get the user's id
    input_dict = decode_jwt(token)
    auth_user_id = input_dict['u_id']
    # check if the user has added the user to friendlist
    sql = "SELECT * FROM user_friendship_tbl where user_id = ('%s') and friend_id = ('%s')" %(auth_user_id, friendID)
    friends = list(db.execute_query(sql))
    if not friends:
        raise InputError(description="The user is not your friend")
    # check if the user has added the user to blacklist
    sql = "SELECT * FROM user_blacklist_tbl where (user_id = ('%s') and black_id = ('%s')) or (user_id = ('%s') and black_id = ('%s'))" %(auth_user_id, friendID, friendID, auth_user_id)
    blacklist = list(db.execute_query(sql))
    if blacklist:
        raise InputError(description="The user has been added to the black list")
    # update the message status
    sql = "UPDATE chat_tbl SET chat_unread = 0 WHERE receiver_id = ('%s') and sender_id = ('%s')" %(auth_user_id, friendID)
    db.execute_query(sql)
    # get all the message
    sql = "SELECT * FROM chat_tbl where (sender_id = ('%s') and receiver_id = ('%s')) or (sender_id = ('%s') and receiver_id = ('%s'))" %(auth_user_id, friendID, friendID, auth_user_id)
    messages = list(db.execute_query(sql))
    for message in messages:
        # add message information
        sql = "SELECT * FROM user_tbl where user_id = ('%s')" %(message['sender_id'])
        sender = list(db.execute_query(sql))
        message['sender_name'] = sender[0]['user_name']
        message['sender_photo'] = sender[0]['user_profile_photo']
        sql = "SELECT * FROM user_tbl where user_id = ('%s')" %(message['receiver_id'])
        receiver = list(db.execute_query(sql))
        message['receiver_name'] = receiver[0]['user_name']
        message['receiver_photo'] = receiver[0]['user_profile_photo']
    return {
        'messages': messages
    }

def messageSend(token, friendID, message, time, type):
    """
    send a message (image/text) to a friend and return the message id
    :param token: the token of the user who is logged in
    :param friendID: the id of the user who is the friend of the user who is logged in
    :param message: the message to be sent
    :param time: the time when the message is sent
    :param type: the type of the message (image/text)
    :return: the message id
    
    pre-condition: the user has logged in
    pre-condition: the format of the time is correct
    error: InputError - token is invalid
    error: InputError - the user is not your friend
    error: InputError - the user has been added to the black list
    error: InputError - the message is too long
    error: InputError - the message is empty
    """
    # check vaild token
    sql = "SELECT * FROM token_tbl"
    store = list(db.execute_query(sql))
    check_valid_token(token, store)
    # decode the token, get the user's id
    input_dict = decode_jwt(token)
    auth_user_id = input_dict['u_id']
    # check if the user has added the user to friendlist
    sql = "SELECT * FROM user_friendship_tbl where user_id = ('%s') and friend_id = ('%s')" %(auth_user_id, friendID)
    friends = list(db.execute_query(sql))
    if not friends:
        raise InputError(description="The user is not your friend")
    # check if the user has added the user to blacklist
    sql = "SELECT * FROM user_blacklist_tbl where (user_id = ('%s') and black_id = ('%s')) or (user_id = ('%s') and black_id = ('%s'))" %(auth_user_id, friendID, friendID, auth_user_id)
    blacklist = list(db.execute_query(sql))
    if blacklist:
        raise InputError(description="The user has been added to the black list")
    if type == 'text':
        # check if the message is valid
        if len(message) > 1000:
            raise InputError(description="The message is too long")
        if message == '':
            raise InputError(description="The message is empty")
        # send the message
        sql = "INSERT INTO chat_tbl (sender_id, receiver_id, chat_content, chat_date, chat_unread) VALUES ('%s', '%s', '%s', '%s', 1)" %(auth_user_id, friendID, message, time)
        db.execute_query(sql)
    elif type == 'image':
        # check if the message is valid
        
        if message == '':
            raise InputError(description="The message is empty")
        # send the message
        sql = "INSERT INTO chat_tbl (sender_id, receiver_id, chat_image, chat_date, chat_unread) VALUES ('%s', '%s', '%s', '%s', 1)" %(auth_user_id, friendID, message, time)
        db.execute_query(sql)
    # get the message id
    sql = "SELECT * FROM chat_tbl"
    messages = list(db.execute_query(sql))
    message_id = messages[-1]['chat_id']
    return {"message_id": message_id}

def messageRemove(token, messageID):
    """
    remove a message from the database
    :param token: the token of the user who is logged in
    :param messageID: the id of the message to be removed
    :return: {}
    
    pre-condition: the sender of the message have right to remove the message at this moment
    error: InputError - token is invalid
    error: InputError - the message is not valid
    error: InputError - the user is not the sender
    """
    # check vaild token
    sql = "SELECT * FROM token_tbl"
    store = list(db.execute_query(sql))
    check_valid_token(token, store)
    # decode the token, get the user's id
    input_dict = decode_jwt(token)
    auth_user_id = input_dict['u_id']
    # check if the message is valid
    sql = "SELECT * FROM chat_tbl where chat_id = ('%s')" %(messageID)
    messages = list(db.execute_query(sql))
    if not messages:
        raise InputError(description="The message is not valid")
    # check if the user is the sender
    if messages[0]['sender_id'] != auth_user_id:
        raise InputError(description="The user is not the sender")
    # remove the message
    sql = "DELETE FROM chat_tbl where chat_id = ('%s')" %(messageID)
    db.execute_query(sql)
    return {}

def share(token, friendID, url, cover, time, type):
    """
    share the movie/director/cast/user to a friend
    :param token: the token of the user who is logged in
    :param friendID: the id of the user who is the friend of the user who is logged in
    :param url: the url of the movie/director/cast/user
    :param cover: the cover of the movie/director/cast/user
    :param time: the time when the message is sent
    :param type: the type of the message (movie/director/cast/user)
    :return: the message id
    
    pre-condition: the user has logged in
    pre-condition: the format of the time is correct
    error: InputError - token is invalid
    error: InputError - the user is not your friend
    error: InputError - the user has been added to the black list
    error: InputError - the url is not valid"""
    # check vaild token
    sql = "SELECT * FROM token_tbl"
    store = list(db.execute_query(sql))
    check_valid_token(token, store)
    # decode the token, get the user's id
    input_dict = decode_jwt(token)
    auth_user_id = input_dict['u_id']
    # check if the user has added the user to friendlist
    sql = "SELECT * FROM user_friendship_tbl where user_id = ('%s') and friend_id = ('%s')" %(auth_user_id, friendID)
    friends = list(db.execute_query(sql))
    if not friends:
        raise InputError(description="The user is not your friend")
    # check if the user has added the user to blacklist
    sql = "SELECT * FROM user_blacklist_tbl where (user_id = ('%s') and black_id = ('%s')) or (user_id = ('%s') and black_id = ('%s'))" %(auth_user_id, friendID, friendID, auth_user_id)
    blacklist = list(db.execute_query(sql))
    if blacklist:
        raise InputError(description="The user has been added to the black list")
    # check if the url is valid
    if not re.match(r'^http[s]?://', url):
        raise InputError(description="The url is not valid")
    # send the message
    sql = "INSERT INTO chat_tbl (sender_id, receiver_id, chat_image, chat_date, chat_unread) VALUES ('%s', '%s', '%s', '%s', 1)" %(auth_user_id, friendID, cover, time)
    db.execute_query(sql)
    if type == "movie":
        sql = "INSERT INTO chat_tbl (sender_id, receiver_id, chat_content, chat_date, chat_unread) VALUES ('%s', '%s', '%s', '%s', 1)" %(auth_user_id, friendID, "movie: " + url, time)
        db.execute_query(sql)
    elif type == "director":
        sql = "INSERT INTO chat_tbl (sender_id, receiver_id, chat_content, chat_date, chat_unread) VALUES ('%s', '%s', '%s', '%s', 1)" %(auth_user_id, friendID, "director: " + url, time)
        db.execute_query(sql)
    elif type == "cast":
        sql = "INSERT INTO chat_tbl (sender_id, receiver_id, chat_content, chat_date, chat_unread) VALUES ('%s', '%s', '%s', '%s', 1)" %(auth_user_id, friendID, "cast: " + url, time)
        db.execute_query(sql)
    elif type == "user":
        sql = "INSERT INTO chat_tbl (sender_id, receiver_id, chat_content, chat_date, chat_unread) VALUES ('%s', '%s', '%s', '%s', 1)" %(auth_user_id, friendID, "user: " + url, time)
        db.execute_query(sql)
    # get the message id
    sql = "SELECT * FROM chat_tbl"
    messages = list(db.execute_query(sql))
    message_id = messages[-1]['chat_id']
    return {"message_id": message_id}

def share_movie(token, friendID, url, cover, time):
    return share(token, friendID, url, cover, time, "movie")

def share_director(token, friendID, url, cover, time):
    return share(token, friendID, url, cover, time, "director")

def share_cast(token, friendID, url, cover, time):
    return share(token, friendID, url, cover, time, "cast")

def share_user(token, friendID, url, cover, time):
    return share(token, friendID, url, cover, time, "user")

def messageUnread(token):
    """check the number of unread messages for the user
    :param token: the token of the user who is logged in
    :return: the number of unread messages
    
    pre-condition: the user has logged in
    pre-condition: check this function ervery certain minute
    error: InputError - token is invalid
    """
    sql = "SELECT * FROM token_tbl"
    store = list(db.execute_query(sql))
    check_valid_token(token, store)
    # decode the token, get the user's id
    input_dict = decode_jwt(token)
    auth_user_id = input_dict['u_id']
    # get the unread messages
    sql = "SELECT * FROM chat_tbl where receiver_id = ('%s') and chat_unread = 1" %(auth_user_id)
    messages = list(db.execute_query(sql))
    return {"unread_messages": len(messages)}