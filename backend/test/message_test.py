import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config.configFlask as config

def testmessageDisplay():
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
    
    result = requests.get(config.url + 'message/list', params = {'token': token1, 'friend_id': 2})
    assert result.status_code == 400
    result = requests.post(config.url + 'blacklist/add', json = {'token': token1, 'black_id': 2})
    assert result.status_code == 200
    result = requests.post(config.url + 'friendlist/add', json = {'token': token1, 'friend_id': 2, 'time': '2020-11-11 11:11:11'})
    assert result.status_code == 400
    result = requests.post(config.url + 'blacklist/remove', json = {'token': token1, 'black_id': 2})
    assert result.status_code == 200
    result = requests.post(config.url + 'friendlist/add', json = {'token': token1, 'friend_id': 2, 'time': '2020-11-11 11:11:11'})
    assert result.status_code == 200
    result = requests.get(config.url + 'message/list', params = {'token': token1, 'friend_id': 2})
    assert result.status_code == 200
    data = result.json()
    assert len(data['messages']) == 1
    assert data['messages'][0]['sender_id'] == 1
    assert data['messages'][0]['receiver_id'] == 2
    assert data['messages'][0]['sender_name'] != None
    assert data['messages'][0]['receiver_name'] != None
    assert data['messages'][0]['chat_content'] != None
    assert data['messages'][0]['chat_unread'] == 1
    result = requests.get(config.url + 'message/list', params = {'token': token2, 'friend_id': 1})
    assert result.status_code == 200
    data = result.json()
    assert data['messages'][0]['chat_unread'] == 0

def testmessageSend():
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
    result = requests.post(config.url + 'message/send', json = {'token': token1, 'friend_id': 2, 'message': 'hello', 'time': '2020-10-10 10:10:10', 'type': 'text'})
    assert result.status_code == 200
    result = requests.get(config.url + 'message/list', params = {'token': token1, 'friend_id': 2})
    assert result.status_code == 200
    data = result.json()

    assert len(data['messages']) == 2
    assert data['messages'][0]['sender_id'] == 1
    assert data['messages'][0]['receiver_id'] == 2
    assert data['messages'][0]['sender_name'] != None
    assert data['messages'][0]['receiver_name'] != None
    assert data['messages'][0]['chat_content'] != None
    assert data['messages'][0]['chat_unread'] == 1
    assert data['messages'][1]['sender_id'] == 1
    assert data['messages'][1]['receiver_id'] == 2
    assert data['messages'][1]['chat_content'] == 'hello'
    assert data['messages'][1]['chat_image'] == None
    assert data['messages'][1]['chat_date'] == '2020-10-10 10:10:10'
    assert data['messages'][1]['chat_unread'] == 1
    result = requests.post(config.url + 'message/send', json = {'token': token1, 'friend_id': 2, 'message': 'hello', 'time': '2020-10-10 10:10:10', 'type': 'image'})
    assert result.status_code == 200
    result = requests.get(config.url + 'message/list', params = {'token': token1, 'friend_id': 2})
    assert result.status_code == 200
    data = result.json()
    assert data['messages'][2]['sender_id'] == 1
    assert data['messages'][2]['receiver_id'] == 2
    assert data['messages'][2]['chat_image'] == 'hello'
    assert data['messages'][2]['chat_content'] == None

    assert data['messages'][2]['chat_date'] == '2020-10-10 10:10:10'
    assert data['messages'][2]['chat_unread'] == 1
    result = requests.get(config.url + 'message/list', params = {'token': token2, 'friend_id': 1})
    assert result.status_code == 200
    data = result.json()
    assert data['messages'][0]['chat_unread'] == 0
    assert data['messages'][1]['chat_unread'] == 0
    assert data['messages'][2]['chat_unread'] == 0


def testmessageRemove():
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
    result = requests.get(config.url + 'message/list', params = {'token': token1, 'friend_id': 2})
    assert result.status_code == 200
    data = result.json()
    assert len(data['messages']) == 1
    assert data['messages'][0]['sender_id'] == 1
    assert data['messages'][0]['receiver_id'] == 2
    assert data['messages'][0]['sender_name'] != None
    assert data['messages'][0]['receiver_name'] != None
    assert data['messages'][0]['chat_content'] != None
    assert data['messages'][0]['chat_unread'] == 1
    result = requests.post(config.url + 'message/delete', json = {'token': token1, 'friend_id': 2, 'message_id': 1})
    assert result.status_code == 200
    result = requests.get(config.url + 'message/list', params = {'token': token1, 'friend_id': 2})
    assert result.status_code == 200
    data = result.json()
    assert len(data['messages']) == 0
    result = requests.get(config.url + 'message/list', params = {'token': token2, 'friend_id': 1})
    assert result.status_code == 200
    data = result.json()
    assert len(data['messages']) == 0

def testmessageShare():
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
    result = requests.post(config.url + 'message/share/movie', json = {'token': token1, 'friend_id': 2, 'url': 'http://hello', 'cover': 'hello', 'time': '2020-10-10 10:10:10', 'type': 'text'})
    assert result.status_code == 200
    result = requests.get(config.url + 'message/list', params = {'token': token1, 'friend_id': 2})
    assert result.status_code == 200
    data = result.json()
    #assert data == 0
    assert len(data['messages']) == 3
    assert data['messages'][0]['chat_unread'] == 1
    assert data['messages'][1]['chat_unread'] == 1
    assert data['messages'][1]['chat_image'] == 'hello'
    assert data['messages'][1]['chat_content'] == None
    assert data['messages'][2]['chat_unread'] == 1
    assert data['messages'][2]['chat_image'] == None
    assert data['messages'][2]['chat_content'] == 'movie: http://hello'
    result = requests.post(config.url + 'message/share/director', json = {'token': token1, 'friend_id': 2, 'url': 'http://hello', 'cover': 'hello', 'time': '2020-10-10 10:10:10', 'type': 'text'})
    assert result.status_code == 200
    result = requests.get(config.url + 'message/list', params = {'token': token1, 'friend_id': 2})
    assert result.status_code == 200
    data = result.json()
    assert len(data['messages']) == 5
    assert data['messages'][3]['chat_unread'] == 1
    assert data['messages'][3]['chat_image'] == 'hello'
    assert data['messages'][3]['chat_content'] == None
    assert data['messages'][4]['chat_unread'] == 1
    assert data['messages'][4]['chat_image'] == None
    assert data['messages'][4]['chat_content'] == 'director: http://hello'
    result = requests.post(config.url + 'message/share/cast', json = {'token': token1, 'friend_id': 2, 'url': 'http://hello', 'cover': 'hello', 'time': '2020-10-10 10:10:10', 'type': 'text'})
    assert result.status_code == 200
    result = requests.get(config.url + 'message/list', params = {'token': token1, 'friend_id': 2})
    assert result.status_code == 200
    data = result.json()
    assert len(data['messages']) == 7
    assert data['messages'][5]['chat_unread'] == 1
    assert data['messages'][5]['chat_image'] == 'hello'
    assert data['messages'][5]['chat_content'] == None
    assert data['messages'][6]['chat_unread'] == 1
    assert data['messages'][6]['chat_image'] == None
    assert data['messages'][6]['chat_content'] == 'cast: http://hello'
    result = requests.post(config.url + 'message/share/user', json = {'token': token1, 'friend_id': 2, 'url': 'http://hello', 'cover': 'hello', 'time': '2020-10-10 10:10:10', 'type': 'text'})
    assert result.status_code == 200
    result = requests.get(config.url + 'message/list', params = {'token': token1, 'friend_id': 2})
    assert result.status_code == 200
    data = result.json()
    assert len(data['messages']) == 9
    assert data['messages'][7]['chat_unread'] == 1
    assert data['messages'][7]['chat_image'] == 'hello'
    assert data['messages'][7]['chat_content'] == None
    assert data['messages'][8]['chat_unread'] == 1
    assert data['messages'][8]['chat_image'] == None
    assert data['messages'][8]['chat_content'] == 'user: http://hello'