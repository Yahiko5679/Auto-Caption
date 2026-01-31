from aiohttp import web
import asyncio
from config import Rkn_Botz

Rkn_AutoCaptionBot = web.RouteTableDef()


@Rkn_AutoCaptionBot.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response(
        {"status": "ok", "bot": "Rkn_AutoCaptionBot"}
    )


async def web_server():
    app = web.Application(client_max_size=30_000_000)
    app.add_routes(Rkn_AutoCaptionBot)

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(
        runner,
        host="0.0.0.0",
        port=Rkn_Botz.PORT
    )
    await site.start()

    print(f"🌐 Web server running on port {Rkn_Botz.PORT}")