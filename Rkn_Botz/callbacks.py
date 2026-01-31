from pyrogram import filters
from pyrogram.types import CallbackQuery
from bot import Bot
from keyboards import start_buttons

@Bot.on_callback_query(filters.regex("^help_cb$"))
async def help_callback(_, query: CallbackQuery):
    await query.message.edit_text(
        """
🆘 <b>Help Guide</b>

📌 Just send media  
📌 Caption added automatically  
📌 Works best in private chat  

Need support?
Join help group 👇
        """,
        reply_markup=start_buttons(),
        disable_web_page_preview=True
    )