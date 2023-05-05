# aiohttpdemo_polls/routes.py
from views import routes
from aiohttp import web


def setup_routes(app: web.Application):
    app.router.add_routes(routes)