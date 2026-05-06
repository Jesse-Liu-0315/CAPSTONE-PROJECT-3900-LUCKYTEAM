from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import json
import smtplib
import random
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

def passwordreset(email, new_password):
    """
    Given a user's email, reset their password to a new password
    :param email: the email of the user
    :param new_password: the new password of the user
    :return: {}

    pre-condition: the email is valid
    pre-condition: the new password is valid
    pre-condition: the action is verified by the user
    error: InputError - email is invalid
    error: InputError - new password is too short

    """
    # check whether this email has been registered
    sql = "SELECT * FROM user_tbl where user_email = '{}'".format(email)
    store = list(db.execute_query(sql))
    if len(store) != 0:
        if len(new_password) < 6:
            raise InputError("Too Short Password")
        sql1 = "UPDATE user_tbl SET user_password = '{}' WHERE user_email = '{}'".format(hash(new_password), email)
        mysql_operate.db.execute_db(sql1)
        return {}
    raise InputError("Invalid Email")

def login(email, password):
    """
    Given a registered user's email and password, generate a valid token for the user to remain authenticated
    :param email: the email of the user
    :param password: the password of the user
    :return: {
        'token': token,
        'auth_user_id': auth_user_id,
    }

    pre-condition: 
    error: InputError - email is invalid
    error: InputError - password is invalid
    """
    sql = "SELECT * FROM user_tbl"
    store = list(db.execute_query(sql))
    for user in store:
        if email == user['user_email'] and hash(password) == user['user_password']:
            # generate token
            user_info = {}
            user_info['u_id'] = user['user_id']
            user_info['session_id'] = generate_new_session_id()
            token = encode_jwt(user_info)
            print('login token encode_jwt: ', token)
            #print(type(token))
            # insert token into database
            sql = "INSERT INTO token_tbl (token) VALUES (%s)"
            para = (token)
            db.execute_query(sql, para)
            print('login return token: ', str(token))
            return {
                'token': str(token),
                'auth_user_id': 1,
            }
    raise InputError("Invalid Email or Password")

def signin(email, password):
    """
    Given a user's email and password, register them as a new user and return a new token for authentication in their session
    generate the default name
    :param email: the email of the user
    :param password: the password of the user
    :return: {
        'token': token,
        'auth_user_id': auth_user_id,
    }

    pre-condition: the database is started
    error: InputError - email is invalid
    error: InputError - password is invalid

    """
    # check email and password whether valid
    check_valid_email(email)
    if len(password) < 6:
        raise InputError("Too Short Password")
    
    # insert user into database
    sql = "INSERT INTO user_tbl(user_email, user_password, user_permission, user_sex, user_age, user_views) VALUES (%s, %s, 'user', 'Undefined', 0, 0)"
    para = (email, hash(password))
    db.execute_query(sql,para)

    # get the new user's id
    sql = "SELECT * FROM user_tbl"
    store = list(db.execute_query(sql))
    new_auth_user_id = store[-1]['user_id']
    # set default username
    sql = "UPDATE user_tbl SET user_name = 'user%s' WHERE user_id = %s"
    para = (new_auth_user_id, new_auth_user_id)
    db.execute_query(sql,para)
    # login and get the token
    token = login(email, password)['token']
    print('signin get token from login: ', token)
    return {
        'token': token,
        'auth_user_id': new_auth_user_id,
    }

def logout(token):
    """
    Given an active token, invalidates the token to log the user out
    :param token: the token of the user
    :return: {}
    
    pre-condition: 
    error: InputError - token is invalid
    """
    sql = "SELECT * FROM token_tbl"
    store = list(db.execute_query(sql))
    check_valid_token(token, store)
    sql = "DELETE FROM token_tbl WHERE token = '{}'".format(token)
    db.execute_query(sql)
    return {}

def verify(email):
    """
    Given a user's email, send a verification code to the user's email
    :param email: the email of the user
    :return: {}
    
    pre-condition: secretmark2021@gmail.com can send email
    error: InputError - email is invalid
    """
    check_valid_email_format(email)
    reset_code = str(random.randint(100000, 999999))
    mail_content = f'''
                    <h1>
                        Hello Dear !<br>
                        How are you today ?
                    </h1>
                    <hr>
                    <h2>
                        We've detected someone trying to sign in or reset password in our website.<br>
                        Please make sure it is your own operation.<br>
                        Your verification code is <strong>{reset_code}</strong>.<br>
                        Please don't tell this code to others.<br>
                        Have a good day.<br>
                    </h2>
                    <hr>
                    <h3>
                        Thank you.<br><br>
                        Best regards,<br>
                        H18B Lucky Team MovieFinder<br>
                    </h3>
                    '''
    # the mail addresses and password
    sender_address = 'secretmark2021@gmail.com'
    sender_pass = 'uptdwrcuwaedhrre'
    receiver_address = email
    # setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Verify your email'
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'html', 'utf-8'))
    # create SMTP session for sending the mail and use gmail with port
    session = smtplib.SMTP('smtp.gmail.com', 587)
    # enable security
    session.starttls()
    # login with mail_id and password
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    return {
        'reset_code': reset_code,
    }




# helper function
# check email whether valid
def check_valid_email(email):
    sql = "SELECT * FROM user_tbl WHERE user_email = '{}'".format(email)
    store = list(db.execute_query(sql))
    # test for the format of e-mail
    if not re.fullmatch(REGEX, email):
        raise InputError("Invalid Email")
    # test this email is whether been used or not
    if len(store) != 0:
        raise InputError("Used Email")
    
# check email format
def check_valid_email_format(email):
    if not re.fullmatch(REGEX, email):
        raise InputError("Invalid Email")