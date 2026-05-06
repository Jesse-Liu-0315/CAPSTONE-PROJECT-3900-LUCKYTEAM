import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config.configFlask as config

def testmovieDetail():
    #result_login_user1 = requests.get(config.url + 'movie', params = {'movieID': 1, 'token': ''})
    result_login_user1 = requests.get(config.url + 'movie?movieID=2&token=')
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert len(data_login_user1['star']) != 0
    assert len(data_login_user1['director']) != 0
    assert data_login_user1['watched'] == False
    assert data_login_user1['wish'] == False
    assert data_login_user1['movie']['movie_id'] == 2
    assert data_login_user1['numWish'] == 0
    assert data_login_user1['numWatched'] == 0
    assert data_login_user1['review'] == []
    assert data_login_user1['recommendation'] != []
    assert data_login_user1['movie_u_may_like'] != []
    movie_views = data_login_user1['movie']['movie_views']
    result_login_user1 = requests.get(config.url + 'movie', params = {'movieID': 2, 'token': ''})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert data_login_user1['movie']['movie_views'] == movie_views + 1

def testmovieDetailWithToken():
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
    result = requests.post(config.url + 'wishlist/add', json = {'token': token, 'movie_id': 1})
    assert result.status_code == 200
    result_login_user1 = requests.get(config.url + 'movie', params = {'movieID': 1, 'token': token})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert data_login_user1['watched'] == True
    assert data_login_user1['wish'] == True
    assert data_login_user1['numWish'] == 1
    assert data_login_user1['numWatched'] == 1
    assert data_login_user1['review'] == []
    assert data_login_user1['recommendation'] != []
    assert data_login_user1['movie_u_may_like'] != []
    assert data_login_user1['movie']['movie_views'] == 0


def testmovieDetailWithToken2():
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
    result_login_user1 = requests.get(config.url + 'movie', params = {'movieID': 1, 'token': token1})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert data_login_user1['review'][0]['content'] == 'test'
    assert data_login_user1['review'][0]['rating_point'] == 5
    assert data_login_user1['review'][0]['review_date'] == '2020-01-01'
    assert data_login_user1['review'][0]['user_id'] == 2
    assert data_login_user1['review'][0]['movie_id'] == 1
    assert data_login_user1['review'][0]['review_id'] == 1
    assert data_login_user1['review'][0]['permission'] == False
    assert data_login_user1['review'][0]['review_like'] == 0
    assert data_login_user1['review'][0]['review_dislike'] == 0
    assert data_login_user1['review'][0]['user_profile_photo'] == None
    assert data_login_user1['review'][0]['user_name'] == 'user2'

    result_login_user1 = requests.get(config.url + 'movie', params = {'movieID': 1, 'token': token2})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert data_login_user1['review'][0]['permission'] == True

    result = requests.post(config.url + 'blacklist/add', json = {'token': token1, 'black_id': 2})
    assert result.status_code == 200
    result_login_user1 = requests.get(config.url + 'movie', params = {'movieID': 1, 'token': token1})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert data_login_user1['review'] == []

def testmovieDetailWithToken3():
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
    result_login_user1 = requests.get(config.url + 'movie', params = {'movieID': 1, 'token': token1})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert data_login_user1['review'][0]['permission'] == False
    result_login_user1 = requests.get(config.url + 'movie', params = {'movieID': 1, 'token': token2})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert data_login_user1['review'][0]['permission'] == True
    

def testmovieSearch():
    requests.post(config.url + 'clear', json = {})
    result_login_user1 = requests.post(config.url + 'search/movie', json = {'keyword': 'the', 'page': 1, 'sortBy': 'Rating: High to Low'})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert len(data_login_user1['movies']) != 0
    assert data_login_user1['movies'][0]['movie_rating'] == 0
    assert data_login_user1['movies'][0]['numReview'] == 0

    result_login_user1 = requests.post(config.url + 'search/movie', json = {'keyword': 'the', 'page': 1, 'sortBy': 'Rating: Low to High'})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert len(data_login_user1['movies']) != 0
    result_login_user1 = requests.post(config.url + 'search/movie', json = {'keyword': 'the', 'page': 1, 'sortBy': 'Review: More to Less'})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert len(data_login_user1['movies']) != 0
    result_login_user1 = requests.post(config.url + 'search/movie', json = {'keyword': 'the', 'page': 1, 'sortBy': 'Review: Less to More'})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert len(data_login_user1['movies']) != 0
    result_login_user1 = requests.post(config.url + 'search/movie', json = {'keyword': 'the', 'page': 1, 'sortBy': 'Release: New to Old'})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert len(data_login_user1['movies']) != 0
    result_login_user1 = requests.post(config.url + 'search/movie', json = {'keyword': 'the', 'page': 1, 'sortBy': 'Release: Old to New'})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert len(data_login_user1['movies']) != 0
    result_login_user1 = requests.post(config.url + 'search/movie', json = {'keyword': 'the', 'page': 1, 'sortBy': 'Name: Z to A'})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert len(data_login_user1['movies']) != 0
    result_login_user1 = requests.post(config.url + 'search/movie', json = {'keyword': 'the', 'page': 1, 'sortBy': 'Name: A to Z'})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert len(data_login_user1['movies']) != 0
    result_login_user1 = requests.post(config.url + 'search/movie', json = {'keyword': 'the', 'page': 1, 'sortBy': 'Views: More to Less'})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert len(data_login_user1['movies']) != 0
    result_login_user1 = requests.post(config.url + 'search/movie', json = {'keyword': 'the', 'page': 1, 'sortBy': 'Views: Less to More'})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert len(data_login_user1['movies']) != 0
    result_login_user1 = requests.post(config.url + 'search/movie', json = {'keyword': '"the" "god"', 'page': 1, 'sortBy': 'BestMatch'})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert len(data_login_user1) != 0

    result_login_user1 = requests.post(config.url + 'search/movie', json = {'keyword': 'the -"gord"', 'page': 1, 'sortBy': 'BestMatch'})
    assert result_login_user1.status_code == 200
    data_login_user1 = result_login_user1.json()
    assert len(data_login_user1) != 0