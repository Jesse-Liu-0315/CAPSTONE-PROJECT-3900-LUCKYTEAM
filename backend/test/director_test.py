import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config.configFlask as config

def testdirectorDetail():
    result_login_user1 = requests.get(config.url + 'director', params = {'directorID': 1})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert data_login_user1['director']['director_id'] == 1
    assert len(data_login_user1['movie']) != 0
    director_views = data_login_user1['director']['director_views']
    result_login_user1 = requests.get(config.url + 'director', params = {'directorID': 1})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert data_login_user1['director']['director_views'] == director_views + 1
    assert data_login_user1['movie'][0]['numOfReviews'] == 0

def testdirectorSearch():
    result_login_user1 = requests.post(config.url + 'search/director', json = {'keyword': 'Tom', 'page': 1, 'sortBy': 'Name: A to Z'})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert len(data_login_user1['directors']) != 0
    result_login_user1 = requests.post(config.url + 'search/director', json = {'keyword': 'Tom', 'page': 1, 'sortBy': 'Name: Z to A'})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert len(data_login_user1['directors']) != 0
    assert data_login_user1['numPages'] != 0
    result_login_user1 = requests.post(config.url + 'search/director', json = {'keyword': 'Tom', 'page': 1, 'sortBy': 'Performances: Less to More'})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert len(data_login_user1['directors']) != 0
    result_login_user1 = requests.post(config.url + 'search/director', json = {'keyword': 'Tom', 'page': 1, 'sortBy': 'Performances: More to Less'})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert len(data_login_user1['directors']) != 0
    result_login_user1 = requests.post(config.url + 'search/director', json = {'keyword': 'Tom', 'page': 1, 'sortBy': 'Views: Less to More'})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert len(data_login_user1['directors']) != 0
    result_login_user1 = requests.post(config.url + 'search/director', json = {'keyword': 'Tom', 'page': 1, 'sortBy': 'Views: More to Less'})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert len(data_login_user1['directors']) != 0
    result_login_user1 = requests.post(config.url + 'search/director', json = {'keyword': 'the', 'page': 1, 'sortBy': 'Age: Old to Young'})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert len(data_login_user1['directors']) != 0
    result_login_user1 = requests.post(config.url + 'search/director', json = {'keyword': 'the', 'page': 1, 'sortBy': 'Age: Young to Old'})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert len(data_login_user1['directors']) != 0
