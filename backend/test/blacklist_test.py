import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config.configFlask as config

def testblacklistDisplay():
    requests.post(config.url + 'clear', json = {})
    user1 = {
        'email': '1@qq.com',
        'password': '111111',
    }
    result_login_user1 = requests.post(config.url + 'auth/register', json = user1)
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    token = data_login_user1['token']
    result = requests.get(config.url + 'blacklist', params = {'token': token})
    assert result.status_code == 200
    data = result.json()
    assert data['blacklist'] == []

# cannot add the user who is in friendlist
def testblacklistAdd():
    requests.post(config.url + 'clear', json = {})
    user1 = {
        'email': '1@qq.com',
        'password': '111111',
    }
    user2 = {
        'email': '2@qq.com',
        'password': '111111',
    }
    result_login_user1 = requests.post(config.url + 'auth/register', json = user1)
    assert result_login_user1.status_code == 200
    result_login_user2 = requests.post(config.url + 'auth/register', json = user2)
    assert result_login_user2.status_code == 200
    data_login_user1 = result_login_user1.json()
    token = data_login_user1['token']
    result = requests.post(config.url + 'blacklist/add', json = {'token': token, 'black_id': 2})
    assert result.status_code == 200
    result = requests.get(config.url + 'blacklist', params = {'token': token})
    assert result.status_code == 200
    data = result.json()
    assert data['blacklist'][0]['user_id'] == 2
    assert data['blacklist'][0]['friend_num'] == 0
    assert data['blacklist'][0]['user_email'] == '2@qq.com'

    result = requests.post(config.url + 'blacklist/add', json = {'token': token, 'black_id': 2})
    assert result.status_code == 400

# cannot add the user repeatedly
def testblacklistAdd2():
    requests.post(config.url + 'clear', json = {})
    user1 = {
        'email': '1@qq.com',
        'password': '111111',
    }
    user2 = {
        'email': '2@qq.com',
        'password': '111111',
    }
    result_login_user1 = requests.post(config.url + 'auth/register', json = user1)
    assert result_login_user1.status_code == 200
    result_login_user2 = requests.post(config.url + 'auth/register', json = user2)
    assert result_login_user2.status_code == 200
    data_login_user1 = result_login_user1.json()
    token = data_login_user1['token']
    result = requests.post(config.url + 'friendlist/add', json = {'token': token, 'friend_id': 2, 'time': "2020-11-11 11:11:11"})
    assert result.status_code == 200
    result = requests.post(config.url + 'blacklist/add', json = {'token': token, 'black_id': 2})
    assert result.status_code == 400

def testblacklistRemove():
    requests.post(config.url + 'clear', json = {})
    user1 = {
        'email': '1@qq.com',
        'password': '111111',
    }
    user2 = {
        'email': '2@qq.com',
        'password': '111111',
    }
    result_login_user1 = requests.post(config.url + 'auth/register', json = user1)
    assert result_login_user1.status_code == 200
    result_login_user2 = requests.post(config.url + 'auth/register', json = user2)
    assert result_login_user2.status_code == 200
    data_login_user1 = result_login_user1.json()
    token = data_login_user1['token']
    result = requests.post(config.url + 'blacklist/add', json = {'token': token, 'black_id': 2, 'time': "2020-11-11 11:11:11"})
    assert result.status_code == 200
    result = requests.post(config.url + 'blacklist/remove', json = {'token': token, 'black_id': 2})
    assert result.status_code == 200
    result = requests.get(config.url + 'blacklist', params = {'token': token})
    assert result.status_code == 200
    data = result.json()
    assert data['blacklist'] == []
    result = requests.post(config.url + 'blacklist/remove', json = {'token': token, 'black_id': 2})
    assert result.status_code == 400