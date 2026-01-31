from pyrogram import types
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery
from config import MythicBots


def start_buttons():
    return types.InlineKeyboardMarkup(
        [
            [
                types.InlineKeyboardButton(
                    "📢 Main Channel",
                    url="https://t.me/MythicBots"
                ),
                types.InlineKeyboardButton(
                    "❓ Help Group",
                    url="https://t.me/+SARTthPIKCcxZTc1"
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
                    url="https://t.me/VoidXTora"
                )
            ]
        ]
    )


# Callback handler of help [help_cb]
@Client.on_callback_query(filters.regex("^help_cb$"))
async def help_callback(client, query: CallbackQuery):
    await query.message.edit_text(
        MythicBots.HELP_TEXT,
        reply_markup=start_buttons(),
        disable_web_page_preview=True
    )