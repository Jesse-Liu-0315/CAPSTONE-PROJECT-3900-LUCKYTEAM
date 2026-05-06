from common import mysql_operate

def clear():
    sql = "set foreign_key_checks = 0"
    mysql_operate.db.execute_db(sql)
    sql = "TRUNCATE user_tbl"
    mysql_operate.db.execute_db(sql)
    sql = "TRUNCATE token_tbl"
    mysql_operate.db.execute_db(sql)
    sql = "TRUNCATE movie_watchlist_tbl"
    mysql_operate.db.execute_db(sql)
    sql = "TRUNCATE user_blacklist_tbl"
    mysql_operate.db.execute_db(sql)
    sql = "TRUNCATE movie_wishlist_tbl"
    mysql_operate.db.execute_db(sql)
    sql = "TRUNCATE user_friendship_tbl"
    mysql_operate.db.execute_db(sql)
    sql = "TRUNCATE chat_tbl"
    mysql_operate.db.execute_db(sql)
    sql = "TRUNCATE movie_review_tbl"
    mysql_operate.db.execute_db(sql)
    sql = "UPDATE movie_tbl SET movie_views = 0"
    mysql_operate.db.execute_db(sql)
    sql = "UPDATE director_tbl SET movie_views = 0"
    mysql_operate.db.execute_db(sql)
    sql = "UPDATE star_tbl SET star_views = 0"
    mysql_operate.db.execute_db(sql)
    sql = "UPDATE movie_tbl SET movie_rating = 0"
    mysql_operate.db.execute_db(sql)
    sql = "set foreign_key_checks = 1"
    mysql_operate.db.execute_db(sql)
    return {}