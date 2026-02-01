from pyrogram import Client, filters, errors, types
from pyrogram.types import Message
from config import MythicBotz 
from .callbacks import start_buttons
from config import Rkn_Botz
import os


@Client.on_message(filters.command("help") & filters.private)
async def help_cmd(client, message: Message):
    await message.reply_text(
        MythicBotz.HELP_TEXT,
        reply_markup=start_buttons(),
        disable_web_page_preview=True
    )



"""
@Client.on_message(filters.command("logs") & filters.user(Rkn_Botz.ADMIN))
async def send_logs(client, message):
    """
    Send bot log file (Render / Local / VPS safe)
    """

    possible_logs = [
        "BotLog.txt",
        "bot.log",
        "app.log",
        "logs.txt"
    ]

    for log_file in possible_logs:
        if os.path.exists(log_file):
            try:
                return await message.reply_document(
                    document=log_file,
                    caption=f"📄 <b>Bot Logs</b>\n\nFile: <code>{log_file}</code>"
                )
            except Exception as e:
                return await message.reply(f"❌ Failed to send log:\n<code>{e}</code>")

    await message.reply(
        "⚠️ <b>No log file found.</b>\n\n"
        "Checked:\n"
        "• BotLog.txt\n"
        "• bot.log\n"
        "• app.log\n"
        "• logs.txt"
    )"""

@Client.on_message(filters.command("logs") & filters.user(Rkn_Botz.ADMIN))
async def logs_cmd(client, message):
    try:
        with open("BotLog.txt", "r", encoding="utf-8", errors="ignore") as f:
            data = f.read()

        if not data.strip():
            return await message.reply("⚠️ Log file is empty")

        # Telegram text limit safe cut
        await message.reply_text(
            data[-4000:],
            disable_web_page_preview=True
        )

    except Exception as e:
        await message.reply(f"❌ Failed to send log:\n<code>{e}</code>")