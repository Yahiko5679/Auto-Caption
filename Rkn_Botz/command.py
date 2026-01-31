from pyrogram import Client, filters, errors, types
from pyrogram.types import Message
from bot import Bot
from keyboards import start_buttons

@Client.on_message(filters.command("help") & filters.private)
async def help_cmd(_, message: Message):
    await message.reply_text(
        """
🆘 <b>Help Menu</b>

• Send any video / document  
• Bot auto adds caption  
• Supports HTML formatting  
• Fast & simple  

Use buttons below 👇
        """,
        reply_markup=start_buttons(),
        disable_web_page_preview=True
    )