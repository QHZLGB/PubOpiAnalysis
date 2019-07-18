from .setting import *
import pymysql


class Operation(object):

    def __init__(self):
        self.host = MYSQL_HOST
        self.port = MYSQL_PORT
        self.user = MYSQL_USER
        self.pwd = MYSQL_PWD
        self.db = MYSQL_DB
        self.conn = None

    def connection(self):
        conn = pymysql.connect(host=self.host, port=self.port, user=self.user,
                               passwd=self.pwd, db=self.db, charset='utf8')
        if conn:
            print('MySQL database opened successfully!')
            self.conn = conn
        else:
            print('MySQL database opened failed!')

    def query(self, sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        # print(result)
        return result

    def close(self):
        self.conn.close()
        print('MySQL database close successful!')

