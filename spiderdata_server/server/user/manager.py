"""
用户管理模块业务代码
"""


class User(object):
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.uuid = None

    def check_password(self, password):
        pass

    def check_token(self, token):
        pass

    def generate_token(self):
        pass

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
    pass


def get_user_by_username(username):
    pass


def get_user_by_email(email):
    pass


def get_user_by_token(token):
    pass
