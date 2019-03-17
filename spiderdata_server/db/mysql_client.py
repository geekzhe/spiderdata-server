"""
Mysql 客户端
"""
import pymysql
import uuid

from spiderdata_server.etc import settings as CONF
from spiderdata_server.server import helper


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
            print('Select %d lines' % cursor.rowcount)
            cursor.close()
            self.conn.commit()
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

    def add_user(self, username, password, email):
        user_uuid = str(uuid.uuid4())
        create_time = helper.get_time()
        # TODO: 处理插入异常
        self.insert('user', (user_uuid, create_time, username, password,
                             email),
                    '(uuid, create_time, username, password, email)')

    def update_user(self):
        pass

    def get_user(self, username=None, user_uuid=None):
        user_info = None
        if username:
            condition = 'username=\'%s\'' % username
        elif user_uuid:
            condition = 'uuid=\'%s\'' % user_uuid
        results = self.select('user', '*', condition)
        if results:
            u = results[0]
            user_info = {
                'uuid': u[0],
                'create_time': u[1],
                'update_time': u[2],
                'username': u[3],
                'password': u[4],
                'birthday': u[5],
                'email': u[6],
                'active': u[7]
            }
        else:
            # TODO(blkart): raise UserNotFound Exception
            pass

        return user_info

    def add_profile(self, user_uuid):
        # TODO: 需要与 add_user 写到同一个事务中
        profile_uuid = helper.generate_uuid()
        create_time = helper.get_time()
        # TODO: 处理异常
        self.insert('user_work_info', (profile_uuid, create_time, user_uuid),
                    '(uuid,create_time,user_uuid)')

    def get_profile(self, user_uuid):
        user_profile = None
        table = 'user inner join user_work_info ' \
                'on user.uuid=user_work_info.user_uuid'
        field = 'username,email,birthday,work_start,education,work_city'
        condition = 'user.uuid=\'%s\'' % user_uuid
        results = self.select(table, field, condition)

        if results:
            p = results[0]
            user_profile = {
                'username': p[0],
                'email': p[1],
                'birthday': p[2],
                'work_start': p[3],
                'education': p[4],
                'work_city': p[5]
            }

        return user_profile

    def update_profile(self, user_uuid, update_profiles):
        table = 'user_work_info'
        assigments = ','.join(['%s=\'%s\'' % (k, v) for k, v
                               in update_profiles.items()])
        condition = 'user_uuid=\'%s\'' % user_uuid
        self.update(table, assigments, condition)

    def add_token(self, user_uuid, token, expire):
        self.insert('user_tokens', (user_uuid, token, expire),
                    '(user_uuid, token,expire)')

    def delete_token(self, token):
        self.update('user_tokens', 'deleted=\'1\'', 'token=\'%s\'' % token)

    def get_token_by_token(self, token):
        t = None
        condition = 'token=\'%s\' and deleted=\'0\'' % token
        results = self.select('user_tokens', '*', condition)

        if results:
            r = results[0]
            t = {
                'user_uuid': r[0],
                'token': r[1],
                'expire': r[2]
            }

        return t
