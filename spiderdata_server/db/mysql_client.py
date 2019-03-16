"""
Mysql 客户端
"""
import pymysql

from spiderdata_server.etc import settings as CONF


class MysqlBase(object):
    """数据库操作基本类，包含与业务无关的数据库操作方法"""
    def __init__(self, host, user, passwd, dbname):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.dbname = dbname
        self.conn = self.connect()

    def connect(self):
        conn = pymysql.connect(self.host, self.user, self.passwd, self.dbname)
        return conn

    def insert(self, table, values, fields=None):
        if fields:
            sql = 'INSERT INTO {table} {fields} VALUES {values}'.format(
                table=table, fields=fields, values=values)
        else:
            sql = 'INSERT INTO {table} VALUES {values}'.format(
                table=table, values=values)

        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            cursor.close()
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print('DataBase Insert Error: %s' % e)
            # TODO(blkart): raise InsertError

    def delete(self, table, condition):
        sql = 'DELETE FROM {table} WHERE {condition}'.format(
            table=table, condition=condition
        )

        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            cursor.close()
            self.conn.commit()
        except Exception as e:
            print('DataBase Delete Error: %s' % e)
            # TODO(blkart): raise DeleteError

    def update(self, table, assignments, condition):
        sql = 'UPDATE {table} SET {assignments} WHERE {condition}'.format(
            table=table, assignments=assignments, condition=condition
        )

        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            cursor.close()
            self.conn.commit()
        except Exception as e:
            print('DataBase Update Error: %s' % e)
            # TODO(blkart): raise UpdateError

    def select(self, table, fields, condition, order_by=None, limit=None,
               desc=False):
        sql = 'SELECT {fields} from {table} WHERE {condition}'.format(
            fields=fields, table=table, condition=condition)

        if order_by:
            sql = sql + ' ORDER BY {order_by}'.format(order_by=order_by)

        if desc:
            sql = sql + ' DESC'

        if limit:
            sql = sql + ' LIMIT {limit}'.format(limit=limit)

        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            print('Select %d lines' % cursor.rowcount)
            return results
        except Exception as e:
            print('DataBase Select Error: %s' % e)
            # TODO(blkart): raise SelectError


class MysqlClient(MysqlBase):
    """与业务有关的数据库操作方法类"""
    def __init__(self):
        host = CONF.MYSQL_HOST
        user = CONF.MYSQL_USERNAME
        passwd = CONF.MYSQL_PASSWORD
        dbname = CONF.MYSQL_DATABASE_NAME
        super().__init__(host, user, passwd, dbname)

    def add_user(self):
        pass

    def update_user(self):
        pass

    def get_user(self):
        pass
