# aiohttpdemo_polls/views.py
import subprocess
from aiohttp import web
from database import add_history

routes = web.RouteTableDef()

@routes.get("/")
async def index(request):
    return web.FileResponse("./public/index.html")
    # return web.Response(text='Hello Aiohttp!')


@routes.post("/webhook")
async def handle_hook(request: web.Request):
    _json = await request.json()
    trigger = _json['trigger']
    exit_code = subprocess.call("bash ./sync_publish.sh", shell=True, cwd="../")
    if exit_code != 0:
        return web.Response(text="sync failed")
    
    _id = add_history(trigger, request.remote)
    return web.Response(text=f'hook success, id:{_id}')
