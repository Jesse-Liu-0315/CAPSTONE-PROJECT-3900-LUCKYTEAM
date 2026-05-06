from flask import Flask   # 需自行下载Flask包，并导入这几个内容
from flask import jsonify
from flask import request
from json import dumps
from flask_caching import Cache
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#from backend.common import mysql_operate  # 从common包中导入mysql_operate，使用其db
#from backend.config import configFlask  # 从config包中导入configFlask
from common import mysql_operate  # 从common包中导入mysql_operate，使用其db
from config import configFlask  # 从config包中导入configFlask
from flask_cors import CORS
import common.createDB as createDB

import auth
import user_pofile
import movie
import wishList
import alreadySeenList
import blackList
import director
import cast
import user
import friendList
import message
import review
import index
import clear 

app = Flask(__name__)
# 初始化生成一个app对象，这个对象就是Flask的当前实例对象，后面的各个方法调用都是这个实例
# Flask会进行一系列自己的初始化，比如web API路径初始化，web资源加载，日志模块创建等。然后返回这个创建好的对象给你

# 解决跨域问题
CORS(app, resources=r'/*')

# 配置缓存
app.config['CACHE_TYPE'] = 'simple'
cache = Cache(app)

@app.route("/")    # 自定义路径
@cache.cached(timeout=60)
def api():
    return 'Hello!'


@app.route("/index", methods = ['GET'])
@cache.cached(timeout=60)
def ind():
    return index.index()

# Regisrer a new user
@app.route("/auth/register", methods = ['POST'])
def register():
    data = request.get_json()
    result = auth.signin(data['email'], data['password'])
    return result

# Login the target user
@app.route("/auth/login", methods = ['POST'])
def login():
    data = request.get_json()
    result = auth.login(data['email'], data['password'])
    return result

# reset the password of the target user
@app.route("/auth/resetpassword", methods = ['POST'])
def passwordreset():
    data = request.get_json()
    result = auth.passwordreset(data['email'], data['password'])
    return result

# Logout the target user
@app.route("/auth/logout", methods = ['POST'])
def logout():
    data = request.get_json()
    result = auth.logout(data['token'])
    return result

# verify the email
@app.route("/auth/verify", methods = ['GET'])
def verify():
    data = request.args.get('email')
    result = auth.verify(data)
    return result

# Get the own user_profile
@app.route("/user_pofile/", methods = ['GET'])
def user_pofile_self():
    data = request.args.get('token')
    result = user_pofile.user_pofile_self(data)
    return result

# change the own user_profile
@app.route("/user_pofile/submit", methods = ['POST'])
def user_pofile_self_submit():
    data = request.get_json()
    result = user_pofile.user_profile_self_submit(data['token'], data['email'], data['name_first'], data['name_last'], data['user_age'], data['user_sex'], data['user_occupation'], data['user_area'], data['user_description'], data['user_profile_photo'])
    return result

# wishlist
@app.route("/wishlist/other", methods= ['GET'])
def wishlistOther():
    data = request.args.get('user_id')
    result = wishList.wishlistOther(data)
    return result

@app.route("/wishlist", methods= ['GET'])
def wishlistDis():
    data = request.args.get('token')
    result = wishList.wishlistDisplay(data)
    return result

@app.route("/wishlist/add", methods= ['POST'])
def wishlistAdd():
    data = request.get_json()
    result = wishList.wishlistAdd(data['token'], data['movie_id'])
    return result

@app.route("/wishlist/remove", methods= ['POST'])
def wishlistRem():
    data = request.get_json()
    result = wishList.wishlistRemove(data['token'], data['movie_id'])
    return result

# watched list
@app.route("/watchedlist/other", methods= ['GET'])
def watchedlistOther():
    data = request.args.get('user_id')
    result = alreadySeenList.alreadyseenlistOther(data)
    return result

@app.route("/watchedlist", methods= ['GET'])
def watchedlistDis():
    data = request.args.get('token')
    result = alreadySeenList.alreadyseenlistDisplay(data)
    return result

@app.route("/watchedlist/add", methods= ['POST'])
def watchedlistAdd():
    data = request.get_json()
    result = alreadySeenList.alreadyseenlistAdd(data['token'], data['movie_id'])
    return result

@app.route("/watchedlist/remove", methods= ['POST'])
def watchedlistRem():
    data = request.get_json()
    result = alreadySeenList.alreadyseenlistRemove(data['token'], data['movie_id'])
    return result

# black list
@app.route("/blacklist", methods= ['GET'])
def blacklistDis():
    data = request.args.get('token')
    result = blackList.blacklistDisplay(data)
    return result

@app.route("/blacklist/add", methods= ['POST'])
def blacklistAdd():
    data = request.get_json()
    result = blackList.blacklistAdd(data['token'], data['black_id'])
    return result

@app.route("/blacklist/remove", methods= ['POST'])
def blacklistRem():
    data = request.get_json()
    result = blackList.alreadyseenlistRemove(data['token'], data['black_id'])
    return result

# friend list
@app.route("/friendlist", methods= ['GET'])
def friendlistDis():
    data = request.args.get('token')
    result = friendList.friendlistDisplay(data)
    return result

@app.route("/friendlist/add", methods= ['POST'])
def friendlistAdd():
    data = request.get_json()
    result = friendList.friendlistAdd(data['token'], data['friend_id'], data['time'])
    return result

@app.route("/friendlist/remove", methods= ['POST'])
def friendlistRem():
    data = request.get_json()
    result = friendList.friendlistRemove(data['token'], data['friend_id'])
    return result

# movie search
@app.route("/search/movie", methods= ['POST'])
def search_movies():
    data = request.get_json()
    result = movie.movie_search(data['keyword'], data['page'], data['sortBy'])
    return result

# movie detail
@app.route("/movie", methods = ['GET'])
#@cache.cached(timeout=1)
def movie_detail_interface():
    data1 = request.args.get('movieID')
    data2 = request.args.get('token')
    result = movie.movie_detail(data1, data2)
    return result

# director search
@app.route("/search/director", methods= ['POST'])
def search_directors():
    data = request.get_json()
    result = director.director_search(data['keyword'], data['page'], data['sortBy'])
    return result

# director
@app.route("/director", methods = ['GET'])
def director_info():
    data = request.args.get('directorID')
    result = director.director_detail(data)
    return result

# cast search
@app.route("/search/cast", methods= ['POST'])
def search_casts():
    data = request.get_json()
    result = cast.cast_search(data['keyword'], data['page'], data['sortBy'])
    return result

# cast detail
@app.route("/cast", methods = ['GET'])
def cast_info():
    data = request.args.get('castID')
    result = cast.cast_detail(data)
    return result

# user search
@app.route("/search/user", methods= ['POST'])
def search_users():
    data = request.get_json()
    result = user.user_search(data['keyword'], data['page'], data['token'], data['sortBy'])
    return result

# user detail
@app.route("/user", methods = ['GET'])
def user_info():
    data1 = request.args.get('userID')
    data2 = request.args.get('token')
    result = user.user_detail(data1, data2)
    return result

# message list
@app.route("/message/list", methods= ['GET'])
def message_list():
    data1 = request.args.get('token')
    data2 = request.args.get('friend_id')
    result = message.messageList(data1, data2)
    return result

# get the number of unread messages
@app.route("/message/unread", methods= ['GET'])
def message_unread():
    data = request.args.get('token')
    result = message.messageUnread(data)
    return result

# message send
@app.route("/message/send", methods= ['POST'])
def message_send():
    data = request.get_json()
    result = message.messageSend(data['token'], data['friend_id'], data['message'], data['time'], data['type'])
    return result

# message delete
@app.route("/message/delete", methods= ['POST'])
def message_delete():
    data = request.get_json()
    result = message.messageRemove(data['token'], data['message_id'])
    return result

# share movie
@app.route("/message/share/movie", methods = ['POST'])
def share_movie():
    data = request.get_json()
    result = message.share_movie(data['token'], data['friend_id'], data['url'], data['cover'], data['time'])
    return result

# share director
@app.route("/message/share/director", methods = ['POST'])
def share_director():
    data = request.get_json()
    result = message.share_director(data['token'], data['friend_id'], data['url'], data['cover'], data['time'])
    return result

# share cast
@app.route("/message/share/cast", methods = ['POST'])
def share_cast():
    data = request.get_json()
    result = message.share_cast(data['token'], data['friend_id'], data['url'], data['cover'], data['time'])
    return result

# share user
@app.route("/message/share/user", methods = ['POST'])
def share_user():
    data = request.get_json()
    result = message.share_user(data['token'], data['friend_id'], data['url'], data['cover'], data['time'])
    return result

# review add
@app.route("/review/add", methods = ['POST'])
def review_add():
    data = request.get_json()
    result = review.add_review(data['movie_id'], data['token'],
                               data['content'],  data['rating'], data['time'])
    return result

# review like
@app.route("/review/like", methods = ['POST'])
def review_like():
    data = request.get_json()
    result = review.like_review(data['movie_id'], data['review_id'])
    return result

# review dislike
@app.route("/review/dislike", methods = ['POST'])
def review_dislike():
    data = request.get_json()
    result = review.dislike_review(data['movie_id'], data['review_id'])
    return result

# review delete
@app.route("/review/delete", methods = ['POST'])
def review_delete():
    data = request.get_json()
    result = review.delete_review(data['movie_id'], data['review_id'], data['token'])
    return result

# add tag for user as the admin
@app.route("/user/addtag", methods = ['POST'])
def tag_add():
    data = request.get_json()
    result = user.user_addTag(data['user_id'], data['token'], data['tag'])
    return result



# clear
@app.route("/clear", methods= ['POST'])
def clearfun():
    result = clear.clear()
    return result


if __name__ == '__main__':
    createDB.createDB()


    app.run(debug=True, host='127.0.0.1', port=configFlask.port)   #
# flask默认是没有开启debug模式的，开启debug模式，可以帮助我们查找代码里面的错误
# host = '127.0.0.1' 表示设置的ip，如果需要连接手机等设备，可以将手机和电脑连接同一个热点，将host设置成对应的ip
# port 为端口号，可自行设置