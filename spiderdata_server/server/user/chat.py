import json

from flask import Flask, g, make_response, request

from spiderdata_server.server import helper
from spiderdata_server.server.user import manager as user_manager

app = Flask(__name__)

# 该列表用于存储在线用户信息(以下注释中统一叫做<在线用户列表>)
# 格式：[{'src_user':'当前连接用户','dest_user':'目标聊天用户','sock':'连接套接字'}]
ONLINE_USERS = []


@app.route('/v1/chat/<dest_user>')
def chat(dest_user):
    # 获取连接对象(web socket)，该连接对象用于与客户端(浏览器)的交互
    # 交互指消息的接收(receive)、发送(send)
    ws = request.environ.get('wsgi.websocket')

    # 验证用户token，验证失败，端开连接
    if not verify_token(request.args.get('token')):
        # TODO(zhe): 返回具体的认证失败的原因(例如token过期等)
        resp = {
            'status': 30002,
            'msg': 'Token authentication failed',
            'body': {}
        }
        ws.send(json.dumps(resp))
        ws.close()
        return make_response('Token authentication failed')

    # 目标用户(dest_user)不存在，则断开连接
    if not user_manager.user_exists(dest_user):
        resp = {
            'status': 30003,
            'msg': 'Target user %s does not exist' % dest_user,
            'body': {}
        }
        ws.send(json.dumps(resp))
        ws.close()
        return make_response('User not found')

    # 获取本次连接的用户名
    src_user = g.user.username

    # 将连接信息添加到在线用户列表中
    conn_info = {
        'src_user': src_user,
        'dest_user': dest_user,
        'user_socket': ws
    }
    print('User %s connected.' % src_user)
    ONLINE_USERS.append(conn_info)
    print('Online user list: %s' % ONLINE_USERS)

    # 检查对端用户是否在线，如果在线，向对端发送当前用户上线通知
    if peer_user_online(src_user, dest_user):
        content = {
            'user': src_user
        }
        # CODE: 30098 用户上线通知
        send_msg_to_user(src_user, dest_user, content, 30098,
                         'Target user %s login' % src_user)
        # 同时向源用户发送对端用户在线的通知
        send_msg_to_user(dest_user, src_user, content, 30098,
                         'Target user %s login' % dest_user)

    # TODO: 从数据库中查找是否存在未发送的离线消息(has_send为False)
    # 如果有，则将消息发送给客户端

    # 循环接收客户端发送过来的消息并处理
    while True:
        # 将接收到的消息赋值给 recv_data
        recv_data = ws.receive()
        print('Receive msg from %s: %s' % (src_user, recv_data))

        # 如果接收到的消息为空，则判断为客户端端开连接(离线)
        # 此时将用户从在线字典中移除，关闭ws，退出等待消息的循环
        if not recv_data:
            print('User %s disconnected.' % src_user)
            ONLINE_USERS.remove(conn_info)
            ws.close()
            # 检查对端用户是否在线，如果在线，向对端发送当前用户离线通知
            if peer_user_online(src_user, dest_user):
                content = {
                    'user': src_user
                }
                # CODE: 30099 用户离线通知
                send_msg_to_user(src_user, dest_user, content, 30099,
                                 'Target user %s logout' % src_user)
            return make_response('User Exit')

        # 将接收到的数据由字符串转换为字典
        recv_msg = json.loads(recv_data)

        # TODO: 将消息存储到数据库中
        # 需要明确数据库有哪些字段
        # id,dest_user,src_user,msg,recv_time,has_send
        # id: 消息ID
        # dest_user: 收信人
        # src_user: 发信人
        # msg: 消息内容
        # recv_time: 服务器接收到消息的时间(也可以理解为客户端发送消息的时间)
        # has_send: 是否已转发给目标用户(默认False，未转发)
        recv_time = helper.get_time()

        # 如果对端用户在线，将消息发送给对端用户
        if peer_user_online(src_user, dest_user):
            # 组织发送给客户端的消息
            send_msg = {
                'msg': recv_msg['msg'],
                'from_user': src_user,
                'send_time': recv_time
            }
            send_msg_to_user(src_user, dest_user, send_msg)

            # 以站内信的方式通知用户收到来自于用户的新消息
            g.user.add_message('来自于 %s 的新消息' % src_user)


def verify_token(token):
    g.user = None
    if user_manager.check_token(token):
        g.user = user_manager.get_user_by_token(token)
        return True
    return False


def peer_user_online(src_user, dest_user):
    for user_info in ONLINE_USERS:
        if user_info['src_user'] == dest_user and \
                user_info['dest_user'] == src_user:
            print('Source user: %s Destination User: %s is online' %
                  (user_info['src_user'], user_info['dest_user']))
            return True
    print('Source user: %s Destination User: %s is not online' %
          (dest_user, src_user))
    return False


def send_msg_to_user(src_user, dest_user, content, status=30001, msg='OK'):
    # 消息不为空时，处理消息
    # 从在线用户列表中查找收信人，如果收信人在线，则将消息发送给用户
    # 在线用户列表格式：
    # [{'src_user':'tom','dest_user':'tony','sock':'tom_sock'},
    #  {'src_user':'tony','dest_user':'tom','sock':'tony_sock'},
    #  {'src_user':'tony','dest_user':'jack','sock':'tony_sock'}]
    for user_info in ONLINE_USERS:
        if user_info['src_user'] == dest_user and \
                user_info['dest_user'] == src_user:
            # 收信人在线，将消息发送给收信人
            dest_user_socket = user_info['user_socket']
            send_data = {
                'status': status,
                'msg': msg,
                'body': content
            }
            print('Send msg to %s: %s' % (dest_user, send_data))
            dest_user_socket.send(json.dumps(send_data))
            # TODO: 将数据库中该条消息的发送状态(has_send)修改为已发送(True)
