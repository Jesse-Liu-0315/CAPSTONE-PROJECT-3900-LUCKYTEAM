import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config.configFlask as config

def test_auth_register():
    requests.post(config.url + 'clear', json = {})
    user1 = {
        'email': '1@qq.com',
        'password': '123456',
    }
    user2 = {
        'email': '1@qq.com',
        'password': '123456',
    }
    user3 = {
        'email': '2@qq.com',
        'password': '111111',
    }
    # normal register
    result_register_user1 = requests.post(config.url + 'auth/register', json = user1)
    data_register_user1 = result_register_user1.json()
    assert result_register_user1.status_code == 200
    assert isinstance(data_register_user1['token'], str)
    assert data_register_user1['auth_user_id'] == 1
    # registe the same email
    result_register_user2 = requests.post(config.url + 'auth/register', json = user2)
    assert result_register_user2.status_code == 400
    # normal register
    result_register_user3 = requests.post(config.url + 'auth/register', json = user3)
    data_register_user3 = result_register_user3.json()
    assert result_register_user3.status_code == 200
    assert data_register_user3['auth_user_id'] == 2
    # wrong email format
    user4 = {
        'email': '2qq.com',
        'password': '111111',
    }
    result_register_user4 = requests.post(config.url + 'auth/register', json = user4)
    assert result_register_user4.status_code == 400

def test_auth_login():
    requests.post(config.url + 'clear', json = {})
    # noraml login
    user1 = {
        'email': '1@qq.com',
        'password': '123456',
    }
    requests.post(config.url + 'auth/register', json = user1)
    result_login_user1 = requests.post(config.url + 'auth/login', json = user1)
    data_login_user1 = result_login_user1.json()
    assert result_login_user1.status_code == 200
    assert data_login_user1['auth_user_id'] == 1
    assert isinstance(data_login_user1['token'], str)
    # login with wrong password
    user1_wrong = {
        'email': '1@qq.com',
        'password': '111111',
    }
    result_login_user2 = requests.post(config.url + 'auth/login', json = user1_wrong)
    assert result_login_user2.status_code == 400
    # login with wrong email
    user2 = {
        'email': '2@qq.com',
        'password': '123456',
    }
    result_login_user3 = requests.post(config.url + 'auth/login', json = user2)
    assert result_login_user3.status_code == 400


def test_auth_logout():
    requests.post(config.url + 'clear', json = {})
    user1 = {
        'email': '1@qq.com',
        'password': '123456',
    }
    requests.post(config.url + 'auth/register', json = user1)
    result_login_user1 = requests.post(config.url + 'auth/login', json = user1)
    data_login_user1 = result_login_user1.json()
    token = data_login_user1['token']
    # noraml logout
    result_logout_user1 = requests.post(config.url + 'auth/logout', json = {'token': token})
    assert result_logout_user1.status_code == 200
    # logout with wrong token
    result_logout_user2 = requests.post(config.url + 'auth/logout', json = {'token': 'wrong token'})
    assert result_logout_user2.status_code == 403

def test_auth_passwordreset():
    requests.post(config.url + 'clear', json = {})
    user1 = {
        'email': '1@qq.com',
        'password': '123456',
    }
    user1_new = {
        'email': '1@qq.com',
        'password': '111111',
    }
    requests.post(config.url + 'auth/register', json = user1)
    result_reset_user1 = requests.post(config.url + 'auth/resetpassword', json = user1_new)
    assert result_reset_user1.status_code == 200
    result_login_user1 = requests.post(config.url + 'auth/login', json = user1_new)
    assert result_login_user1.status_code == 200
    # login with pervious password
    result = requests.post(config.url + 'auth/login', json = user1)
    assert result.status_code == 400

