import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config.configFlask as config

def test_userpofile():
    requests.post(config.url + 'clear', json = {})
    user1 = {
        'email': '1@qq.com',
        'password': '111111',
    }
    result_login_user1 = requests.post(config.url + 'auth/register', json = user1)
    assert result_login_user1.status_code == 200
    data_register_user1 = result_login_user1.json()
    token = data_register_user1['token']
    result_user_pofile = requests.get(config.url + 'user_pofile', params = {'token': token})
    data_user_pofile = result_user_pofile.json()
    assert result_user_pofile.status_code == 200
    assert data_user_pofile['email'] == '1@qq.com'
    assert data_user_pofile['name_first'] == None
    assert data_user_pofile['name_last'] == None
    assert data_user_pofile['user_age'] == 0
    assert data_user_pofile['user_sex'] == 'Undefined'
    assert data_user_pofile['user_occupation'] == None
    assert data_user_pofile['user_area'] == None
    assert data_user_pofile['user_description'] == None
    assert data_user_pofile['user_profile_photo'] == None
    assert data_user_pofile['user_views'] == 0
    # not vaild token
    result_user_pofile = requests.get(config.url + 'user_pofile', params = {'token': 'token'})
    assert result_user_pofile.status_code == 403


def test_userpofile_submit():
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
    data_register_user1 = result_login_user1.json()
    token = data_register_user1['token']
    result_login_user2 = requests.post(config.url + 'auth/register', json = user2)
    assert result_login_user2.status_code == 200
    # change the email to another user's email
    result = requests.post(config.url + 'user_pofile/submit', json = {'token': token, 'email':'2@qq.com', 'name_first':'jx', 'name_last':'l', 'user_age':0, 'user_sex':'Undifined', 'user_occupation':'', 'user_area':'', 'user_description':'', 'user_profile_photo': ''})
    assert result.status_code == 400
    # noraml change
    result = requests.post(config.url + 'user_pofile/submit', json = {'token': token, 'email':'1@qq.com', 'name_first':'jx', 'name_last':'l', 'user_age':0, 'user_sex':'Undefined', 'user_occupation':'', 'user_area':'', 'user_description':'', 'user_profile_photo': '**********************************************************************'})
    assert result.status_code == 200
    result_user_pofile = requests.get(config.url + 'user_pofile', params = {'token': token})
    data_user_pofile = result_user_pofile.json()
    assert data_user_pofile['email'] == '1@qq.com'
    assert data_user_pofile['name_first'] == 'jx'
    assert data_user_pofile['name_last'] == 'l'
    assert data_user_pofile['user_age'] == 0
    assert data_user_pofile['user_profile_photo'] == '**********************************************************************'
    assert data_user_pofile['user_views'] == 0
    assert data_user_pofile['user_occupation'] == ''
    assert data_user_pofile['user_area'] == ''
    assert data_user_pofile['user_description'] == ''
    # not vaild token
    result_user_pofile = requests.post(config.url + 'user_pofile/submit', json = {'token': 'token', 'email':'2@qq.com', 'name_first':'jx', 'name_last':'l', 'user_age':0, 'user_sex':'Undifined', 'user_occupation':'', 'user_area':'', 'user_description':'', 'user_profile_photo': ''})
    assert result_user_pofile.status_code == 403