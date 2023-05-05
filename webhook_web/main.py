# coding: utf-8
#

from aiohttp import web
import aiohttp_debugtoolbar
from routes import setup_routes
from settings import config

app = web.Application()
setup_routes(app)
app['config'] = config
aiohttp_debugtoolbar.setup(app)

if __name__ == "__main__":
    web.run_app(app, port=5000)