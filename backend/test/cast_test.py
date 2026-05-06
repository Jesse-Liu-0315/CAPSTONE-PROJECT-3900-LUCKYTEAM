import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config.configFlask as config

def testcastDetail():
    requests.post(config.url + 'clear', json = {})
    result_login_user1 = requests.get(config.url + 'cast', params = {'castID': 1})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert data_login_user1['cast']['star_id'] == 1
    assert len(data_login_user1['movie']) != 0
    star_views = data_login_user1['cast']['star_views']
    result_login_user1 = requests.get(config.url + 'cast', params = {'castID': 1})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert data_login_user1['cast']['star_views'] == star_views + 1
    assert isinstance(data_login_user1['movie'][0]['numOfReviews'], int) == True
    assert data_login_user1['movie'][0]['numOfReviews'] == 0

def testcastSearch():
    result_login_user1 = requests.post(config.url + 'search/cast', json = {'keyword': 'Tom', 'page': 1, 'sortBy': 'Name: A to Z'})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert len(data_login_user1['casts']) != 0
    result_login_user1 = requests.post(config.url + 'search/cast', json = {'keyword': 'Tom', 'page': 1, 'sortBy': 'Name: Z to A'})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert len(data_login_user1['casts']) != 0
    assert data_login_user1['numPages'] != 0
    result_login_user1 = requests.post(config.url + 'search/cast', json = {'keyword': 'Tom', 'page': 1, 'sortBy': 'Performances: Less to More'})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert len(data_login_user1['casts']) != 0
    result_login_user1 = requests.post(config.url + 'search/cast', json = {'keyword': 'Tom', 'page': 1, 'sortBy': 'Performances: More to Less'})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert len(data_login_user1['casts']) != 0
    result_login_user1 = requests.post(config.url + 'search/cast', json = {'keyword': 'Tom', 'page': 1, 'sortBy': 'Views: Less to More'})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert len(data_login_user1['casts']) != 0
    result_login_user1 = requests.post(config.url + 'search/cast', json = {'keyword': 'Tom', 'page': 1, 'sortBy': 'Views: More to Less'})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert len(data_login_user1['casts']) != 0
    result_login_user1 = requests.post(config.url + 'search/cast', json = {'keyword': 'Tom', 'page': 1, 'sortBy': 'Age: Old to Young'})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert len(data_login_user1['casts']) != 0
    result_login_user1 = requests.post(config.url + 'search/cast', json = {'keyword': 'Tom', 'page': 1, 'sortBy': 'Age: Young to Old'})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert len(data_login_user1['casts']) != 0

