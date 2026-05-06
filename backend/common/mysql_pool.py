import pymysql
import pymysqlpool
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.configSQL import MYSQL_HOST,MYSQL_PORT,MYSQL_USER,MYSQL_PASSWD,MYSQL_DB

class Database:
    def __init__(self, **config):
        self.pool = pymysqlpool.ConnectionPool(size=100, name='mypool', **config)

    def execute_query(self, query, params=None):
        with self.pool.get_connection() as conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(query, params)
                rows = cursor.fetchall()
                return rows

db_config = {
    'host': MYSQL_HOST,
    'port': MYSQL_PORT,
    'user': MYSQL_USER,
    'password': MYSQL_PASSWD,
    'database': MYSQL_DB,
    'autocommit': True
}

db = Database(**db_config)
