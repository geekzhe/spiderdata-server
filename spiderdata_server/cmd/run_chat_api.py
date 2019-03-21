from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from spiderdata_server.server.user.chat import app
from spiderdata_server.etc import settings as CONF

chat_server = WSGIServer((CONF.USER_API_HOST, CONF.CHAT_API_PORT), app,
                         handler_class=WebSocketHandler)
chat_server.serve_forever()
