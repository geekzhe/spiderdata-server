from spiderdata_server.server.user.api import app
from spiderdata_server.etc import settings as CONF

app.run(host=CONF.USER_API_HOST, port=CONF.USER_API_PORT)