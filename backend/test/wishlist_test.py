import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config.configFlask as config

def testwishlistDisplay():
    requests.post(config.url + 'clear', json = {})
    user1 = {
        'email': '1@qq.com',
        'password': '111111',
    }
    result_login_user1 = requests.post(config.url + 'auth/register', json = user1)
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    token = data_login_user1['token']
    result = requests.get(config.url + 'wishlist', params = {'token': token})
    assert result.status_code == 200
    data = result.json()
    assert data['wishlist'] == []


def testwishlistAdd():
    requests.post(config.url + 'clear', json = {})
    user1 = {
        'email': '1@qq.com',
        'password': '111111',
    }
    result_login_user1 = requests.post(config.url + 'auth/register', json = user1)
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    token = data_login_user1['token']
    result = requests.post(config.url + 'wishlist/add', json = {'token': token, 'movie_id': 1})
    assert result.status_code == 200
    result = requests.get(config.url + 'wishlist', params = {'token': token})
    assert result.status_code == 200
    data = result.json()
    assert data['wishlist'][0]['movie_id'] == 1
    result = requests.post(config.url + 'wishlist/add', json = {'token': token, 'movie_id': 1})
    assert result.status_code == 400

def testwishlistRemove():
    requests.post(config.url + 'clear', json = {})
    user1 = {
        'email': '1@qq.com',
        'password': '111111',
    }
    result_login_user1 = requests.post(config.url + 'auth/register', json = user1)
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    token = data_login_user1['token']
    result = requests.post(config.url + 'wishlist/add', json = {'token': token, 'movie_id': 1})
    assert result.status_code == 200
    result = requests.post(config.url + 'wishlist/remove', json = {'token': token, 'movie_id': 1})
    assert result.status_code == 200
    result = requests.get(config.url + 'wishlist', params = {'token': token})
    assert result.status_code == 200
    data = result.json()
    assert data['wishlist'] == []
    result = requests.post(config.url + 'wishlist/remove', json = {'token': token, 'movie_id': 1})
    assert result.status_code == 400

def testwishlistOther():
    requests.post(config.url + 'clear', json = {})
    user1 = {
        'email': '1@qq.com',
        'password': '111111',
    }
    result_login_user1 = requests.post(config.url + 'auth/register', json = user1)
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    token = data_login_user1['token']
    result = requests.post(config.url + 'wishlist/add', json = {'token': token, 'movie_id': 1})
    query = {
        'user_id': 1,
    }
    result = requests.get(config.url + 'wishlist/other', params = query)
    assert result.status_code == 200
    data = result.json()
    assert data['wishlist'][0]['movie_id'] == 1
    assert len(data['wishlist']) == 1
    assert data['wishlist'][0]['review_num'] == 0
    query = {
        'user_id': 2,
    }
    result = requests.get(config.url + 'wishlist/other', params = query)
    assert result.status_code == 200
    data = result.json()
    assert data['wishlist'] == []
