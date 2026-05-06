import pymysql
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#from backend.config.configSQL import MYSQL_HOST,MYSQL_PORT,MYSQL_USER,MYSQL_PASSWD,MYSQL_DB
from config.configSQL import MYSQL_HOST,MYSQL_PORT,MYSQL_USER,MYSQL_PASSWD,MYSQL_DB
import pandas as pd
from common.mysql_pool import db

def createDB():
    
    try:
        # 创建游标
        db.execute_query("DROP DATABASE IF EXISTS {};".format(MYSQL_DB))
        db.execute_query("CREATE DATABASE {};".format(MYSQL_DB))
        db.execute_query("USE {};".format(MYSQL_DB))
        # 创建表 user_tbl
        db.execute_query("""CREATE TABLE user_tbl(
                        user_id INT UNSIGNED AUTO_INCREMENT,
                        user_email VARCHAR(64) NOT NULL UNIQUE,
                        user_name VARCHAR(64),
                        user_firstname VARCHAR(32),
                        user_lastname VARCHAR(32),
                        user_age INT,
                        user_sex enum('Male','Female', 'Undefined'),
                        user_occupation VARCHAR(32),
                        user_area VARCHAR(32),
                        user_description VARCHAR(128),
                        user_tag VARCHAR(32),
                        user_permission enum('admin','user'),
                        user_views INT,
                        user_password VARCHAR(128) NOT NULL,
                        user_profile_photo LONGTEXT,
                        PRIMARY KEY ( user_id )
                    );""")
        # 创建表 movie_tbl
        db.execute_query("""CREATE TABLE movie_tbl(
                        movie_id INT UNSIGNED AUTO_INCREMENT,
                        movie_name VARCHAR(128) NOT NULL,
                        movie_release_date INT,
                        movie_language VARCHAR(32),
                        movie_description TEXT,
                        movie_tag VARCHAR(128),
                        movie_views INT,
                        movie_nationality VARCHAR(128),
                        movie_cover VARCHAR(8182),
                        movie_rating FLOAT,
                        PRIMARY KEY ( movie_id )
                    );""")
        # 创建表 director_tbl
        db.execute_query("""CREATE TABLE director_tbl(
                        director_id INT UNSIGNED AUTO_INCREMENT,
                        director_name VARCHAR(64) NOT NULL,
                        director_description TEXT,
                        director_birth VARCHAR(32),
                        director_nationality VARCHAR(128),
                        director_views INT,
                        director_cover VARCHAR(8182),
                        PRIMARY KEY ( director_id )
                    );""")
        # 创建表 direct_in_tbl
        db.execute_query("""CREATE TABLE direct_in_tbl(
                        director_id INT UNSIGNED not null,
                        movie_id INT UNSIGNED not null,
                        PRIMARY KEY ( director_id, movie_id ),
                        foreign key (director_id) references director_tbl(director_id),
                        foreign key (movie_id) references movie_tbl(movie_id)
                    );""")
        # 创建表 movie_wishlist_tbl
        db.execute_query("""CREATE TABLE movie_wishlist_tbl(
                        user_id INT UNSIGNED not null,
                        movie_id INT UNSIGNED not null,
                        PRIMARY KEY ( user_id, movie_id ),
                        foreign key (user_id) references user_tbl(user_id),
                        foreign key (movie_id) references movie_tbl(movie_id)
                    );""")
        # 创建表 movie_watchlist_tbl
        db.execute_query("""CREATE TABLE movie_watchlist_tbl(
                        user_id INT UNSIGNED not null,
                        movie_id INT UNSIGNED not null,
                        PRIMARY KEY ( user_id, movie_id ),
                        foreign key (user_id) references user_tbl(user_id),
                        foreign key (movie_id) references movie_tbl(movie_id)
                    );""")
        # 创建表 user_blacklist_tbl
        db.execute_query("""CREATE TABLE user_blacklist_tbl(
                        user_id INT UNSIGNED not null,
                        black_id INT UNSIGNED not null,
                        PRIMARY KEY ( user_id, black_id ),
                        foreign key (user_id) references user_tbl(user_id),
                        foreign key (black_id) references user_tbl(user_id)
                    );""")
        # 创建表 movie_review_tbl
        db.execute_query("""CREATE TABLE movie_review_tbl(
                        review_id INT UNSIGNED AUTO_INCREMENT,
                        movie_id INT UNSIGNED not null,
                        user_id INT UNSIGNED not null,
                        content VARCHAR(512),
                        rating_point INT,
                        review_date VARCHAR(32),
                        review_like INT,
                        review_dislike INT,
                        PRIMARY KEY ( review_id )
                    );""")
        # 创建表 user_friendship_tbl
        db.execute_query("""CREATE TABLE user_friendship_tbl(
                        user_id INT UNSIGNED not null,
                        friend_id INT UNSIGNED not null,
                        PRIMARY KEY ( user_id, friend_id )
                    );""")
        # 创建表 chat_tbl
        db.execute_query("""CREATE TABLE chat_tbl(
                        chat_id INT UNSIGNED AUTO_INCREMENT,
                        sender_id INT UNSIGNED not null,
                        receiver_id INT UNSIGNED not null,
                        chat_content VARCHAR(512),
                        chat_image LONGTEXT,
                        chat_date VARCHAR(32),
                        chat_unread INT,
                        PRIMARY KEY ( chat_id )
                    );""")
        # 创建表 star_tbl
        db.execute_query("""CREATE TABLE star_tbl(
                        star_id INT UNSIGNED AUTO_INCREMENT,
                        star_name VARCHAR(64) NOT NULL,
                        star_birth VARCHAR(32),
                        star_nationality VARCHAR(128),
                        star_description TEXT,
                        star_views INT,
                        star_cover VARCHAR(8182),
                        PRIMARY KEY ( star_id )
                    );""")
        # 创建表 star_in_tbl
        db.execute_query("""CREATE TABLE star_in_tbl(
                        movie_id INT UNSIGNED not null,
                        star_id INT UNSIGNED not null,
                        PRIMARY KEY ( movie_id, star_id ),
                        foreign key (movie_id) references movie_tbl(movie_id),
                        foreign key (star_id) references star_tbl(star_id)
                    );""")
        # 创建表 token_tbl
        db.execute_query("""CREATE TABLE token_tbl(
                        token VARCHAR(512) NOT NULL,
                        PRIMARY KEY ( token )
                    );""") 
        # 插入数据 MOVIRE_INFO
        df = pd.read_excel("resource/Movie_INFO.xlsx")
        df = df.fillna('NULL')
        for row in df.itertuples():
            # movie_name, movie_date, movie_language, movie_tag, movie_description, movie_img
            sql = "INSERT INTO movie_tbl (movie_name, movie_release_date, movie_language, movie_tag, movie_description, movie_cover, movie_views, movie_rating) VALUES (%s, %s, %s, %s, %s, %s, 0, 0)"
            para = (row.moveie_name, row.moveie_date, row.movie_language, row.movie_tag, row.movie_description, row.movie_img)
            db.execute_query(sql, para)
        
        # 插入数据 Director_INFO
        df = pd.read_excel("resource/Director_INFO.xlsx")
        df = df.fillna('NULL')
        for row in df.itertuples():
            sql = "INSERT INTO director_tbl (director_name, director_description, director_birth, director_nationality, director_cover, director_views) values (%s, %s, %s, %s, %s, 0)"
            para = (row.director_name, row.director_description, row.director_born, row.director_nationality, row.director_img)
            db.execute_query(sql, para)
        
        # 插入数据 Direct_in_tbl
        df = pd.read_excel("resource/Direct_IN_INFO.xlsx")
        df = df.fillna('NULL')
        for row in df.itertuples():
            sql = "INSERT INTO direct_in_tbl (director_id, movie_id) values (%s, %s)"
            para = (row.director_id, row.moveie_id)
            db.execute_query(sql, para)

        # 插入数据 Star_INFO
        df = pd.read_excel("resource/Star_INFO.xlsx")
        df = df.fillna('NULL')
        for row in df.itertuples():
            # star_name, star_description, star_born, star_nationality, star_img
            sql = "INSERT INTO star_tbl (star_name, star_description, star_birth, star_nationality, star_cover, star_views) values (%s, %s, %s, %s, %s, 0)"
            para = (row.star_name, row.star_description, row.star_born, row.star_nationality, row.star_img)
            db.execute_query(sql, para)
        
        # 插入数据 Star_IN_INFO
        df = pd.read_excel("resource/Star_IN_INFO.xlsx")
        df = df.fillna('NULL')
        for row in df.itertuples():
            sql = "INSERT INTO star_in_tbl (movie_id, star_id) values (%s, %s)"
            para = (row.moveie_id, row.star_id)
            db.execute_query(sql, para)


        # connect_timeout: Number of seconds the mysqld server waits for a connect packet before responding with 'Bad handshake'
        # interactive_timeout Number of seconds the server waits for activity on an interactive connection before closing it
        #cwait_timeout Number of seconds the server waits for activity on a connection before closing it
        db.execute_query('SET GLOBAL connect_timeout=28800')
        db.execute_query('SET GLOBAL interactive_timeout=28800')
        db.execute_query('SET GLOBAL wait_timeout=28800')

    except pymysql.err.MySQLError as _error:
        raise _error
    #except:
    #    conn.close()
        #SET ADMIN OPTION
