"""
用户管理模块-接口模块

该模块中只放用于对外提供服务的 RESTful API 接口代码，不放具体的业务逻辑代码
"""
from flask import Flask

app = Flask(__name__)


@app.route('/v1/user', methods=['POST'])
def register():
    """用户注册方法"""
    pass


@app.route('/v1/user/token', methods=['POST'])
def login():
    """用户登陆方法
    验证用户名密码，返回token"""
    pass


@app.route('/v1/user/token', methods=['DELETE'])
def logout():
    """用户退出方法
    退出登陆，销毁token"""
    pass


@app.route('/v1/user/profile', methods=['GET'])
def get_user_profile():
    """获取用户信息"""
    pass


@app.route('/v1/user/profile', methods=['PUT'])
def update_user_profile():
    """更新用户信息"""
    pass


@app.route('/v1/user/skill', methods=['GET'])
def get_user_skill():
    """获取用户技能"""
    pass


@app.route('/v1/user/skill', methods=['PUT'])
def update_user_skill():
    """更新用户技能"""
    pass


@app.route('/v1/user/messages', methods=['GET'])
def get_user_messages():
    """获取用户消息(站内信)"""
    pass


@app.route('/v1/user/messages', methods=['PUT'])
def update_user_message():
    """更新用户消息(站内信)状态"""
    pass


@app.route('/v1/user/account_activation/<activation_code>', methods=['GET'])
def activate_account(activation_code):
    """账号激活(通过激活码)"""
    pass
