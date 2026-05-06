import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config.configFlask as config

def testreviewadd():
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
    result_login_user1 = requests.get(config.url + 'movie', params = {'movieID': 1, 'token': token1})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert data_login_user1['movie']['movie_rating'] == 0

    result_login_user2 = requests.post(config.url + 'review/add', json = {'movie_id': 1, 'token': token2, 'content': 'test', 'rating': 5, 'time': '2020-01-01'})
    assert result_login_user2.status_code == 200
    result_login_user1 = requests.get(config.url + 'movie', params = {'movieID': 1, 'token': token1})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert data_login_user1['review'][0]['content'] == 'test'
    assert data_login_user1['movie']['movie_rating'] == 5
    result_login_user1 = requests.get(config.url + 'movie', params = {'movieID': 1, 'token': token2})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert data_login_user1['review'][0]['content'] == 'test'
    assert data_login_user1['review'][0]['review_like'] == 0
    assert data_login_user1['review'][0]['review_dislike'] == 0

def testreviewremove():
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

    result_login_user2 = requests.post(config.url + 'review/add', json = {'movie_id': 1, 'token': token2, 'content': 'test', 'rating': 5, 'time': '2020-01-01'})
    assert result_login_user2.status_code == 200
    data = result_login_user2.json()
    review_id = data['reviewID']
    result_login_user1 = requests.get(config.url + 'movie', params = {'movieID': 1, 'token': token1})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()    
    assert data_login_user1['movie']['movie_rating'] == 5
    result_login_user1 = requests.post(config.url + 'review/delete', json = {'movie_id': 1, 'review_id': review_id, 'token': token1})
    assert result_login_user1.status_code == 400
    result_login_user1 = requests.post(config.url + 'review/delete', json = {'movie_id': 1, 'review_id': review_id, 'token': token2})
    assert result_login_user1.status_code == 200
    result_login_user1 = requests.post(config.url + 'review/delete', json = {'movie_id': 1, 'review_id': review_id, 'token': token2})
    assert result_login_user1.status_code == 400
    result_login_user1 = requests.get(config.url + 'movie', params = {'movieID': 1, 'token': token1})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()    
    assert data_login_user1['movie']['movie_rating'] == 0

def testreviewlike():
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
    result_login_user2 = requests.post(config.url + 'review/add', json = {'movie_id': 1, 'token': token2, 'content': 'test', 'rating': 5, 'time': '2020-01-01'})
    assert result_login_user2.status_code == 200
    data = result_login_user2.json()
    review_id = data['reviewID']
    result_login_user1 = requests.get(config.url + 'movie', params = {'movieID': 1, 'token': token1})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert data_login_user1['review'][0]['review_like'] == 0

    result_login_user1 = requests.post(config.url + 'review/like', json = {'movie_id': 1, 'review_id': review_id})
    assert result_login_user1.status_code == 200
    result_login_user1 = requests.post(config.url + 'review/like', json = {'movie_id': 1, 'review_id': review_id})
    assert result_login_user1.status_code == 200
    result_login_user1 = requests.get(config.url + 'movie', params = {'movieID': 1, 'token': token1})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert data_login_user1['review'][0]['review_like'] == 2

def testreviewdislike():
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
    result_login_user2 = requests.post(config.url + 'review/add', json = {'movie_id': 1, 'token': token2, 'content': 'test', 'rating': 5, 'time': '2020-01-01'})
    assert result_login_user2.status_code == 200
    data = result_login_user2.json()
    review_id = data['reviewID']
    result_login_user1 = requests.get(config.url + 'movie', params = {'movieID': 1, 'token': token1})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert data_login_user1['review'][0]['review_dislike'] == 0

    result_login_user1 = requests.post(config.url + 'review/dislike', json = {'movie_id': 1, 'review_id': review_id})
    assert result_login_user1.status_code == 200
    result_login_user1 = requests.post(config.url + 'review/dislike', json = {'movie_id': 1, 'review_id': review_id})
    assert result_login_user1.status_code == 200
    result_login_user1 = requests.get(config.url + 'movie', params = {'movieID': 1, 'token': token1})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert data_login_user1['review'][0]['review_dislike'] == 2