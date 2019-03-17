"""
用户管理模块-接口模块

该模块中只放用于对外提供服务的 RESTful API 接口代码，不放具体的业务逻辑代码
"""
from flask import Flask, g, jsonify, make_response, request
from flask_httpauth import HTTPTokenAuth

from spiderdata_server.server import helper
from spiderdata_server.server.user import manager as user_manager

app = Flask(__name__)
token_auth = HTTPTokenAuth('Token')


@app.route('/v1/user', methods=['POST'])
def register():
    """用户注册方法"""
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')

    # TODO: username、password、email合法性检查

    # 判断用户是否存在，用户存在时注册失败，提示用户创建失败
    user = user_manager.get_user_by_username(username)
    if user:
        resp = helper.make_response_dict(10002, 'user exists',
                                         {'username': username})
        return make_response(jsonify(resp), 400)

    # 创建新用户
    # 处理创建时的异常
    user = user_manager.create_user(username, password, email)
    if not user:
        resp = helper.make_response_dict(10003, 'user create failed server '
                                                'internal error',
                                         {'username': username})
        return make_response(jsonify(resp), 500)

    # 将用户对象赋值给 g.user，其它方法中可以通过 g.user 获取用户对象
    g.user = user
    resp = helper.make_response_dict(10001, 'user create success',
                                     {'username': g.user.username})
    return make_response(jsonify(resp), 201)


@app.route('/v1/user/token', methods=['POST'])
def login():
    """用户登陆方法
    验证用户名密码，返回token"""
    username = request.json.get('username')
    password = request.json.get('password')

    # 判断用户是否存在，用户不存在返回错误信息
    user = user_manager.get_user_by_username(username)
    if not user:
        resp = helper.make_response_dict(10004, 'user not found',
                                         {'username': username})
        return make_response(jsonify(resp), 404)

    # 检查密码是否正确，密码不正确返回错误信息
    if not user.check_password(password):
        resp = helper.make_response_dict(10005, 'password incorrect',
                                         {'username': username})
        return make_response(jsonify(resp), 400)

    # 生成并返回 token
    token = user.generate_token()
    if not token:
        resp = helper.make_response_dict(10006, 'token create failed',
                                         {'username': username})
        return make_response(jsonify(resp), 500)

    resp = helper.make_response_dict(10001, 'login success',
                                     {'username': username,
                                      'token': token})
    return make_response(jsonify(resp), 201)


@app.route('/v1/user/token', methods=['DELETE'])
@token_auth.login_required
def logout():
    """用户退出方法
    退出登陆，销毁token"""
    # TODO: 处理异常
    token = request.json.get('token')
    g.user.revoke_token(token)

    resp = helper.make_response_dict(10001, 'logout success',
                                     {'username': g.user.username})
    return make_response(jsonify(resp), 201)


@app.route('/v1/user/profile', methods=['GET'])
@token_auth.login_required
def get_user_profile():
    """获取用户信息"""
    user = user_manager.get_user_by_username(g.user.username)
    user_profile = user.get_profile()

    if not user_profile:
        resp = helper.make_response_dict(10007, 'user profile not found',
                                         {'username': g.user.username})
        return make_response(jsonify(resp), 500)

    resp = helper.make_response_dict(10001, 'success',
                                     {'user_profile': user_profile})
    return make_response(jsonify(resp), 201)


@app.route('/v1/user/profile', methods=['PUT'])
@token_auth.login_required
def update_user_profile():
    """更新用户信息"""
    user = user_manager.get_user_by_username(g.user.username)
    update_profile = request.json
    # TODO: 检查 update_profile 中参数的合法性
    user.update_profile(update_profile)

    user_profile = user.get_profile()
    if not user_profile or \
            not all(map(lambda x, y: update_profile[x] == user_profile[x],
                        update_profile, user_profile)):
        resp = helper.make_response_dict(10008, 'user profile update failed',
                                         {'username': g.user.username})
        return make_response(jsonify(resp), 500)

    resp = helper.make_response_dict(10001, 'success',
                                     {'user_profile': user_profile})
    return make_response(jsonify(resp), 201)


@app.route('/v1/user/skill', methods=['GET'])
@token_auth.login_required
def get_user_skill():
    """获取用户技能"""
    user = user_manager.get_user_by_username(g.user.username)
    user_skill = user.get_skill()

    if not user_skill:
        resp = helper.make_response_dict(10009, 'user skill not found',
                                         {'username': g.user.username})
        return make_response(jsonify(resp), 500)

    resp = helper.make_response_dict(10001, 'success',
                                     {'skill': user_skill})
    return make_response(jsonify(resp), 201)


@app.route('/v1/user/skill', methods=['PUT'])
@token_auth.login_required
def update_user_skill():
    """更新用户技能"""
    user = user_manager.get_user_by_username(g.user.username)
    update_skill = request.json.get('skill')
    user.update_skill(update_skill)

    user_skill = user.get_skill()
    if not user_skill or update_skill != user_skill:
        resp = helper.make_response_dict(10010, 'user skill update failed',
                                         {'username': g.user.username})
        return make_response(jsonify(resp), 500)

    resp = helper.make_response_dict(10001, 'success',
                                     {'skill': user_skill})
    return make_response(jsonify(resp), 201)


@app.route('/v1/user/messages', methods=['GET'])
@token_auth.login_required
def get_user_messages():
    """获取用户消息(站内信)"""
    limit = request.json.get('limit')
    page = request.json.get('page')
    user = user_manager.get_user_by_username(g.user.username)
    messages = user.get_messages(limit, page)

    # TODO: 处理异常
    resp = helper.make_response_dict(10001, 'success', {'messages': messages})
    return make_response(jsonify(resp), 201)


@app.route('/v1/user/messages', methods=['PUT'])
def update_user_message():
    """更新用户消息(站内信)状态"""
    pass


@app.route('/v1/user/account_activation/<activation_code>', methods=['GET'])
def activate_account(activation_code):
    """账号激活(通过激活码)"""
    pass


@token_auth.verify_token
def verify_token(token):
    g.user = None
    if user_manager.check_token(token):
        g.user = user_manager.get_user_by_token(token)
        return True
    return False
