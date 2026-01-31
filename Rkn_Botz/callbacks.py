from pyrogram import types
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery
from Rkn_Botz.keyboards import start_buttons


def start_buttons():
    return types.InlineKeyboardMarkup(
        [
            [
                types.InlineKeyboardButton(
                    "📢 Main Channel",
                    url="https://t.me/Rkn_Bots_Updates"
                ),
                types.InlineKeyboardButton(
                    "❓ Help Group",
                    url="https://t.me/Rkn_Bots_Support"
                )
            ],
            [
                types.InlineKeyboardButton(
                    "🆘 Help",
                    callback_data="help_cb"
                )
            ],
            [
                types.InlineKeyboardButton(
                    "🔥 Source Code",
                    url="https://github.com/RknDeveloper/Rkn-AutoCaptionBot"
                )
            ]
        ]
    )


# Callback handler of help [help_cb]
@Client.on_callback_query(filters.regex("^help_cb$"))
async def help_callback(client, query: CallbackQuery):
    await query.message.edit_text(
        """
🆘 <b>Help Guide</b>

📌 Send media  
📌 Bot adds caption  
📌 Best in private chat  

Need more?
Join help group 👇
        """,
        reply_markup=start_buttons(),
        disable_web_page_preview=True
    )