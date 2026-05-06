import pymysql

#from backend.config.configSQL import MYSQL_HOST,MYSQL_PORT,MYSQL_USER,MYSQL_PASSWD,MYSQL_DB
from config.configSQL import MYSQL_HOST,MYSQL_PORT,MYSQL_USER,MYSQL_PASSWD,MYSQL_DB


class MysqlDb():

    def __init__(self, host, port, user, passwd, db):
        # 建立数据库连接
        self.conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            passwd=passwd,
            db=db
        )
        self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def select_db(self, sql):
        """查询"""
        # 检查连接是否断开，如果断开就进行重连
        self.conn.ping(reconnect=True)
        # 使用 execute() 执行sql
        self.cur.execute(sql)
        # 使用 fetchall() 获取查询结果
        data = self.cur.fetchall()
        if data == tuple():
            return []
        return data

    def __del__(self): # 对象资源被释放时触发，在对象即将被删除时的最后操作
        # 关闭游标
        self.cur.close()
        # 关闭数据库连接
        self.conn.close()

    def execute_db(self, sql):
        """更新/新增/删除"""
        try:
            # 检查连接是否断开，如果断开就进行重连
            self.conn.ping(reconnect=True)
            # 使用 execute() 执行sql
            self.cur.execute(sql)
            # 提交事务
            self.conn.commit()
            return "插入成功"
        except Exception as e:
            # 回滚所有更改
            self.conn.rollback()
            return "操作出现错误"

# 定义一个实例对象，方便别的文件引用其方法
db = MysqlDb(MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWD, MYSQL_DB)
