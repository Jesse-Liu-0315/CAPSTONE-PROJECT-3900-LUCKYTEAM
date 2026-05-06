import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config.configFlask as config

def testalreadyseenlistDisplay():
    requests.post(config.url + 'clear', json = {})
    user1 = {
        'email': '1@qq.com',
        'password': '111111',
    }
    result_login_user1 = requests.post(config.url + 'auth/register', json = user1)
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    token = data_login_user1['token']
    result = requests.get(config.url + 'watchedlist', params = {'token': token})
    assert result.status_code == 200
    data = result.json()
    assert data['watchedlist'] == []


def testalreadyseenlistAdd():
    requests.post(config.url + 'clear', json = {})
    user1 = {
        'email': '1@qq.com',
        'password': '111111',
    }
    result_login_user1 = requests.post(config.url + 'auth/register', json = user1)
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    token = data_login_user1['token']
    result = requests.post(config.url + 'watchedlist/add', json = {'token': token, 'movie_id': 1})
    assert result.status_code == 200
    result = requests.get(config.url + 'watchedlist', params = {'token': token})
    assert result.status_code == 200
    data = result.json()
    assert data['watchedlist'][0]['movie_id'] == 1
    assert data['watchedlist'][0]['review_num'] == 0
    result = requests.post(config.url + 'watchedlist/add', json = {'token': token, 'movie_id': 1})
    assert result.status_code == 400

def testalreadyseenlistRemove():
    requests.post(config.url + 'clear', json = {})
    user1 = {
        'email': '1@qq.com',
        'password': '111111',
    }
    result_login_user1 = requests.post(config.url + 'auth/register', json = user1)
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    token = data_login_user1['token']
    result = requests.post(config.url + 'watchedlist/add', json = {'token': token, 'movie_id': 1})
    assert result.status_code == 200
    result = requests.post(config.url + 'watchedlist/remove', json = {'token': token, 'movie_id': 1})
    assert result.status_code == 200
    result = requests.get(config.url + 'watchedlist', params = {'token': token})
    assert result.status_code == 200
    data = result.json()
    assert data['watchedlist'] == []
    result = requests.post(config.url + 'watchedlist/remove', json = {'token': token, 'movie_id': 1})
    assert result.status_code == 400

def testalreadyseenlistOther():
    requests.post(config.url + 'clear', json = {})
    user1 = {
        'email': '1@qq.com',
        'password': '111111',
    }
    result_login_user1 = requests.post(config.url + 'auth/register', json = user1)
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    token = data_login_user1['token']
    result = requests.post(config.url + 'watchedlist/add', json = {'token': token, 'movie_id': 1})
    query = {
        'user_id': 1,
    }
    result = requests.get(config.url + 'watchedlist/other', params = query)
    assert result.status_code == 200
    data = result.json()
    assert data['watchedlist'][0]['movie_id'] == 1
    assert len(data['watchedlist']) == 1
    assert data['watchedlist'][0]['review_num'] == 0
    query = {
        'user_id': 2,
    }
    result = requests.get(config.url + 'watchedlist/other', params = query)
    assert result.status_code == 200
    data = result.json()
    assert data['watchedlist'] == []
