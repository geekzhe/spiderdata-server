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

    def revoke_token(self, token):
        DB.delete_token(token)

    def get_profile(self):
        user_profile = DB.get_profile(self.uuid)
        return user_profile

    def update_profile(self, update_profiles):
        DB.update_profile(self.uuid, update_profiles)

    def get_skill(self):
        user_skill = DB.get_skill(self.uuid)
        return user_skill

    def update_skill(self, skills):
        DB.update_skill(self.uuid, skills)

    def add_message(self, title, content=None):
        DB.add_message(self.uuid, title, content)

    def get_messages(self, limit=10, page=0):
        messages = DB.get_messages(self.uuid, limit, page)
        return messages

    def update_message_status(self, msg_id):
        DB.update_message(msg_id)

    def delete_message(self, msg_id):
        DB.delete_message(msg_id)

    def get_message_status(self, msg_id):
        msg = DB.get_message(msg_id)
        has_read = msg.get('has_read', '0')
        return has_read

    def message_deleted(self, msg_id):
        msg = DB.get_message(msg_id)
        deleted = msg.get('deleted', '0')
        return deleted

    def generate_activation_code(self):
        pass

    def active_account(self, activation_code):
        pass


def create_user(username, password, email):
    # TODO: 密码需要hash后存储
    # TODO: 捕获数据库操作异常
    DB.add_user(username, password, email)
    user = get_user_by_username(username)
    DB.add_profile(user.uuid)
    DB.add_skill(user.uuid)

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
        print('token %s not found' % token)
        return False

    if helper.expire(rest['expire']):
        print('token %s expire' % token)
        return False

    return True

