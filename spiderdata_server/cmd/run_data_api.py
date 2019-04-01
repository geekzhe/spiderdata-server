#!/usr/bin/env python3
from spiderdata_server.server.data.api import app
from spiderdata_server.etc import settings as CONF

app.run(host=CONF.DATA_API_HOST, port=CONF.DATA_API_PORT)
