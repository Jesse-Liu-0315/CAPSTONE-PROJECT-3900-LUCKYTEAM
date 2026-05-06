import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config.configFlask as config

def testuserdetail():
    requests.post(config.url + 'clear', json = {})
    user1 = {
        'email': '1@qq.com',
        'password': '111111',
    }
    result_login_user1 = requests.post(config.url + 'auth/register', json = user1)
    assert result_login_user1.status_code == 200
    result_login_user1 = requests.get(config.url + 'user', params = {'userID': 1, 'token': ''})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert data_login_user1['user']['user_id'] == 1
    user_views = data_login_user1['user']['user_views']
    result_login_user1 = requests.get(config.url + 'user', params = {'userID': 1, 'token': ''})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert data_login_user1['user']['user_views'] == user_views + 1
    assert data_login_user1['user']['user_id'] == 1
    assert data_login_user1['blacklist'] == False
    assert data_login_user1['friends'] == False

def testuserdetail2():
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
    token1 = data_login_user1['token']
    data_login_user2 = result_login_user2.json()
    token2 = data_login_user2['token']
    result = requests.post(config.url + 'friendlist/add', json = {'token': token1, 'friend_id': 2, 'time': '2020-11-11 11:11:11'})
    assert result.status_code == 200
    result_login_user1 = requests.get(config.url + 'user', params = {'userID': 2, 'token': token1})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert data_login_user1['friends'] == True
    result = requests.post(config.url + 'friendlist/remove', json = {'token': token1, 'friend_id': 2})
    assert result.status_code == 200
    result = requests.post(config.url + 'blacklist/add', json = {'token': token1, 'black_id': 2})
    assert result.status_code == 200
    result_login_user1 = requests.get(config.url + 'user', params = {'userID': 2, 'token': token1})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert data_login_user1['blacklist'] == True

def testusersearch():
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
    token1 = data_login_user1['token']
    result = requests.post(config.url + 'search/user', json = {'keyword': '', 'page': 1, 'token': '', 'sortBy': 'Name: A to Z'})
    assert result.status_code == 200
    data = result.json()
    assert len(data['users']) == 2
    result = requests.post(config.url + 'blacklist/add', json = {'token': token1, 'black_id': 2})
    assert result.status_code == 200

    result = requests.post(config.url + 'search/user', json = {'keyword': '', 'page': 1, 'token': token1, 'sortBy': 'Name: A to Z'})
    assert result.status_code == 200
    data = result.json()
    assert len(data['users']) == 1
    result = requests.post(config.url + 'search/user', json = {'keyword': '', 'page': 1, 'token': token1, 'sortBy': 'Name: Z to A'})
    assert result.status_code == 200
    data = result.json()
    assert len(data['users']) == 1
    result = requests.post(config.url + 'search/user', json = {'keyword': '', 'page': 1, 'token': token1, 'sortBy': 'Views: Less to More'})
    assert result.status_code == 200
    data = result.json()
    assert len(data['users']) == 1
    result = requests.post(config.url + 'search/user', json = {'keyword': '', 'page': 1, 'token': token1, 'sortBy': 'Views: More to Less'})
    assert result.status_code == 200
    data = result.json()
    assert len(data['users']) == 1

def testusersearch2():
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
    token1 = data_login_user1['token']
    result = requests.post(config.url + 'search/user', json = {'keyword': '', 'page': 1, 'token': '', 'sortBy': 'Name: A to Z'})
    assert result.status_code == 200
    data = result.json()
    assert len(data['users']) == 2
    result = requests.post(config.url + 'friendlist/add', json = {'token': token1, 'friend_id': 2, 'time': '2020-11-11 11:11:11'})
    assert result.status_code == 200
    result = requests.post(config.url + 'search/user', json = {'keyword': '', 'page': 1, 'token': token1, 'sortBy': 'Name: A to Z'})
    assert result.status_code == 200
    data = result.json()
    assert len(data['users']) == 2
    assert data['users'][1]['friends'] == True