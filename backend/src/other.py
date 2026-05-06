import hashlib
import jwt
from error import *

SESSION_ID = 0
SECRET = 'SECRETIVE_MARK'

def generate_new_session_id():
    global SESSION_ID
    SESSION_ID += 1
    return SESSION_ID

# check token whether valid
def check_valid_token(token, token_list):
    for to in token_list:
        if to['token'] == token:
            return
    raise AccessError('Invalid Token')



# only used in password and undecipherable
def hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

def encode_jwt(user_info):
    encoded_jwt =  jwt.encode(user_info, SECRET, algorithm = 'HS256')
    if isinstance(encoded_jwt, bytes):
        return encoded_jwt.decode('utf-8')
    else:
        return encoded_jwt

# string as input and dictionary as output
# encoded_token = 'abcdefg'
def decode_jwt(encoded_token):
    return jwt.decode(encoded_token, SECRET, algorithms = 'HS256')