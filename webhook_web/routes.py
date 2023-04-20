# aiohttpdemo_polls/routes.py
from views import index
from aiohttp import web


def setup_routes(app: web.Application):
    app.router.add_get('/', index)