"""
用户管理模块业务代码
"""
from spiderdata_server.db.mysql_client import MysqlClient
from spiderdata_server.server import helper

DB = MysqlClient()


class User(object):
    def __init__(self, username, password, email, uuid=None):
        self.username = username
        self.password = password
        self.email = email
        self.uuid = uuid

    def check_password(self, password):
        if self.password != password:
            return False
        else:
            return True

    def generate_token(self, expire=60):
        # 生成随机 token
        token = helper.generate_uuid()

        # 计算过期时间
        now_sec = helper.get_time_sec()
        expire_time_sec = now_sec + expire * 60
        expire_time = helper.get_time(expire_time_sec)

        # 将 token 存储到数据库
        DB.add_token(self.uuid, token, expire_time)

        if check_token(token):
            return token

    def revoke_token(self):
        pass

    def get_profile(self):
        pass

    def update_profile(self, **kwargs):
        pass

    def get_skill(self):
        pass

    def update_skill(self, skills):
        pass

    def get_messages(self, limit=10, page=1):
        pass

    def update_message_status(self, msg_id):
        pass

    def generate_activation_code(self):
        pass

    def active_account(self, activation_code):
        pass


def create_user(username, password, email):
    # TODO: 密码需要hash后存储
    # TODO: 捕获数据库操作异常
    DB.add_user(username, password, email)
    user = get_user_by_username(username)

    return user


def get_user_by_username(username):
    user = None
    user_info = DB.get_user(username=username)
    if user_info:
        user = User(user_info['username'], user_info['password'],
                    user_info['email'], user_info['uuid'])

    return user


def get_user_by_email(email):
    pass


def get_user_by_token(token):
    user = None
    token_info = DB.get_token_by_token(token)
    user_uuid = token_info['user_uuid']
    user_info = DB.get_user(user_uuid=user_uuid)
    if user_info:
        user = User(user_info['username'], user_info['password'],
                    user_info['email'], user_info['uuid'])

    return user


def check_token(token):
    rest = DB.get_token_by_token(token)
    if not rest:
        return False

    if helper.expire(rest['expire']):
        return False

    return True

