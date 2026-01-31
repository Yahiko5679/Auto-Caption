from pyrogram import Client, filters, errors, types
from pyrogram.types import Message
from config import MythicBots
from .callbacks import start_buttons

@Client.on_message(filters.command("help") & filters.private)
async def help_cmd(client, message: Message):
    await message.reply_text(
        MythicBots.HELP_TEXT,
        reply_markup=start_buttons(),
        disable_web_page_preview=True
    )