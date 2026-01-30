from aiohttp import web
from pyrogram import Client
from config import Rkn_Botz
from Rkn_Botz.web_support import web_server


class Rkn_AutoCaptionBot(Client):
    def __init__(self):
        super().__init__(
            name="Rkn-Advance-Caption-Bot",
            api_id=Rkn_Botz.API_ID,
            api_hash=Rkn_Botz.API_HASH,
            bot_token=Rkn_Botz.BOT_TOKEN,
            workers=200,
            plugins={"root": "Rkn_Botz"},
            sleep_threshold=15,
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.uptime = Rkn_Botz.BOT_UPTIME
        self.force_channel = Rkn_Botz.FORCE_SUB

        if Rkn_Botz.FORCE_SUB:
            try:
                link = await self.export_chat_invite_link(Rkn_Botz.FORCE_SUB)
                self.invitelink = link
            except Exception as e:
                print(e)
                print("Make Sure Bot admin in force sub channel")
                self.force_channel = None

        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, Rkn_Botz.PORT).start()

        print(f"{me.first_name} Iꜱ Sᴛᴀʀᴛᴇᴅ.....✨️")

        # 🔥 ADMIN FIX (ONLY CHANGE)
        admin_ids = Rkn_Botz.ADMIN
        if isinstance(admin_ids, int):
            admin_ids = [admin_ids]

        for admin_id in admin_ids:
            try:
                await self.send_message(
                    admin_id,
                    f"**__{me.first_name} Iꜱ Sᴛᴀʀᴛᴇᴅ.....✨️__**"
                )
            except Exception:
                pass

    async def stop(self, *args):
        await super().stop()
        print("Bot Stopped 🙄")


Rkn_AutoCaptionBot().run()