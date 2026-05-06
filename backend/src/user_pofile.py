import sys
import os
import re
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from other import *
from error import InputError
#from backend.common import mysql_operate
from common import mysql_operate
from common.mysql_pool import db


REGEX = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'

def user_pofile_self(token):
    """
    get the user's information
    :param token: the token of the user
    :return: {
        'email': email,
        'name_first': name_first,
        'name_last': name_last,
        'user_age': user_age,
        'user_sex': user_sex,
        'user_occupation': user_occupation,
        'user_area': user_area,
        'user_description': user_description,
        'user_tag': user_tag,
        'user_profile_photo': user_profile_photo,
        'user_views': user_views
        }
        
    pre-condition: the token is valid
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
    sql = "SELECT * FROM user_tbl"
    store = list(db.execute_query(sql))
    for user in store:
        if user['user_id'] == auth_user_id:
            
            return {
                'email': user['user_email'],
                'name_first': user['user_firstname'],
                'name_last': user['user_lastname'],
                'user_age': user['user_age'],
                'user_sex' : user['user_sex'],
                'user_occupation' : user['user_occupation'],
                'user_area': user['user_area'],
                'user_description': user['user_description'],
                'user_tag': user['user_tag'],
                'user_profile_photo': user['user_profile_photo'],
                'user_views': user['user_views']
            }
    raise InputError("Invalid Token")

def user_profile_self_submit(token, 
                            email, 
                            name_first, 
                            name_last, 
                            user_age, 
                            user_sex, 
                            user_occupation, 
                            user_area, 
                            user_description,
                            user_profile_photo):
    """
    modify the user's information
    :param token: the token of the user
    :param email: the user's email
    :param name_first: the user's first name
    :param name_last: the user's last name
    :param user_age: the user's age
    :param user_sex: the user's sex
    :param user_occupation: the user's occupation
    :param user_area: the user's area
    :param user_description: the user's description
    :param user_profile_photo: the user's profile photo
    :return: {}
    
    pre-condition: the token is valid
    error: InputError - token is invalid
    
    """
    # check whether this token is valid
    sql = "SELECT * FROM token_tbl"
    store = list(db.execute_query(sql))
    check_valid_token(token, store)
    # decode the token, get the user's id
    input_dict = decode_jwt(token)
    auth_user_id = input_dict['u_id']

    # check whether this email is valid
    if not re.fullmatch(REGEX, email):
        raise InputError("Invalid Email")

    sql = "SELECT * FROM user_tbl"
    store = list(db.execute_query(sql))
    # check whether this modified email has been registered
    for user in store:
        if email == user['user_email'] and auth_user_id != user['user_id']:
            raise InputError("Invalid Email or user_id")
    # have a change to modify the user's information
    for user in store:
        if auth_user_id == user['user_id']:
            sql = """UPDATE user_tbl SET user_email = '{}', 
                                        user_firstname = '{}', 
                                        user_lastname = '{}',
                                        user_name = '{}',
                                        user_age = '{}', 
                                        user_sex = '{}', 
                                        user_occupation = '{}', 
                                        user_area = '{}', 
                                        user_description = '{}',
                                        user_profile_photo = '{}'
                                        WHERE user_id = '{}'
                                        """.format(email, name_first, name_last, name_first + ' ' + name_last, user_age, user_sex, user_occupation, user_area, user_description, user_profile_photo, auth_user_id)
            db.execute_query(sql)
            return {}
    raise InputError("Invalid Email or user_id")