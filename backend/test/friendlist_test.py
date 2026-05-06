import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config.configFlask as config

def testfriendlistDisplay():
    requests.post(config.url + 'clear', json = {})
    user1 = {
        'email': '1@qq.com',
        'password': '111111',
    }
    result_login_user1 = requests.post(config.url + 'auth/register', json = user1)
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    token = data_login_user1['token']
    result = requests.get(config.url + 'friendlist', params = {'token': token})
    assert result.status_code == 200
    data = result.json()
    assert data['friendlist'] == []


def testfriendlistAdd():
    requests.post(config.url + 'clear', json = {})
    user1 = {
        'email': '1@qq.com',
        'password': '111111',
    }
    user2 = {
        'email': '2@qq.com',
        'password': '111111',
    }
    user3 = {
        'email': '3@qq.com',
        'password': '111111',
    }

    result_login_user1 = requests.post(config.url + 'auth/register', json = user1)
    assert result_login_user1.status_code == 200
    result_login_user2 = requests.post(config.url + 'auth/register', json = user2)
    assert result_login_user2.status_code == 200
    result_login_user3 = requests.post(config.url + 'auth/register', json = user3)
    assert result_login_user3.status_code == 200
    data_login_user1 = result_login_user1.json()
    token1 = data_login_user1['token']
    data_login_user2 = result_login_user2.json()
    token2 = data_login_user2['token']
    data_login_user3 = result_login_user3.json()
    token3 = data_login_user3['token']
    result = requests.post(config.url + 'friendlist/add', json = {'token': token1, 'friend_id': 2, 'time': '2020-11-11 11:11:11'})
    assert result.status_code == 200
    result = requests.get(config.url + 'friendlist', params = {'token': token1})
    assert result.status_code == 200
    data = result.json()
    assert data['friendlist'][0]['user_id'] == 2
    assert data['friendlist'][0]['last_message_time'] != None
    assert data['friendlist'][0]['unread_num'] == 0
    result = requests.get(config.url + 'friendlist', params = {'token': token2})
    assert result.status_code == 200
    data = result.json()
    assert data['friendlist'][0]['user_id'] == 1
    assert data['friendlist'][0]['last_message_time'] != None
    assert data['friendlist'][0]['unread_num'] == 1

    result = requests.post(config.url + 'friendlist/add', json = {'token': token2, 'friend_id': 3, 'time': '2020-11-11 11:11:11'})
    assert result.status_code == 200

    result = requests.get(config.url + 'friendlist', params = {'token': token2})
    assert result.status_code == 200
    data = result.json()
    assert data['friendlist'][0]['user_id'] == 1
    assert data['friendlist'][0]['last_message_time'] != None
    assert data['friendlist'][0]['unread_num'] == 1

    result = requests.post(config.url + 'friendlist/add', json = {'token': token1, 'friend_id': 2, 'time': '2020-11-11 11:11:11'})
    assert result.status_code == 400
    result = requests.post(config.url + 'friendlist/add', json = {'token': token1, 'friend_id': 1, 'time': '2020-11-11 11:11:11'})
    assert result.status_code == 400
    result = requests.post(config.url + 'blacklist/add', json = {'token': token1, 'black_id': 2})
    assert result.status_code == 400
    result = requests.post(config.url + 'friendlist/remove', json = {'token': token1, 'friend_id': 2})
    assert result.status_code == 200
    result = requests.post(config.url + 'blacklist/add', json = {'token': token2, 'black_id': 1})
    assert result.status_code == 200
    result = requests.post(config.url + 'friendlist/add', json = {'token': token1, 'friend_id': 2, 'time': '2020-11-11 11:11:11'})
    assert result.status_code == 400

    result = requests.post(config.url + 'blacklist/remove', json = {'token': token2, 'black_id': 1})
    assert result.status_code == 200
    result = requests.post(config.url + 'blacklist/add', json = {'token': token1, 'black_id': 2})
    assert result.status_code == 200
    result = requests.post(config.url + 'friendlist/add', json = {'token': token1, 'friend_id': 2, 'time': '2020-11-11 11:11:11'})
    assert result.status_code == 400

def testfriendlistRemove():
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
    result = requests.post(config.url + 'friendlist/add', json = {'token': token, 'friend_id': 2, 'time': '2020-11-11 11:11:11'})
    assert result.status_code == 200
    result = requests.post(config.url + 'friendlist/remove', json = {'token': token, 'friend_id': 2})
    assert result.status_code == 200
    result = requests.get(config.url + 'friendlist', params = {'token': token})
    assert result.status_code == 200
    data = result.json()
    assert data['friendlist'] == []
    result = requests.post(config.url + 'friendlist/remove', json = {'token': token, 'friend_id': 2})
    assert result.status_code == 400