import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config.configFlask as config

def testindex():
    requests.post(config.url + 'clear', json = {})
    
    
    user1 = {
        'email': '1@qq.com',
        'password': '111111',
    }
    result_login_user1 = requests.post(config.url + 'auth/register', json = user1)
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    token1 = data_login_user1['token']
    result_login_user2 = requests.post(config.url + 'review/add', json = {'movie_id': 1, 'token': token1, 'content': 'test', 'rating': 5, 'time': '2020-01-01'})
    assert result_login_user2.status_code == 200
    result_login_user1 = requests.get(config.url + 'index', json = {})
    
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    #assert data_login_user1 == 0
    assert len(data_login_user1['TopRated']) != 0
    assert len(data_login_user1['MostReviewed']) != 0
    assert len(data_login_user1['MostRecent']) != 0
    assert data_login_user1['TopRated'][0]['movie_id'] == 1
    assert data_login_user1['MostReviewed'][0]['movie_id'] == 1