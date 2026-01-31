from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.errors import UserNotParticipant

from config import Rkn_Botz
from .database import rkn_botz


# ─────────────────────────────────────
# 🔐 Force Subscribe Filter (Callable)
# ─────────────────────────────────────
class ForceSubCheck:
    def __init__(self, channel: str):
        # Remove @ if provided
        self.channel = channel.lstrip("@") if channel else None

    async def __call__(self, client: Client, message: Message) -> bool:
        # Safety check
        if not message.from_user:
            return False

        user_id = message.from_user.id

        # Register user in database
        try:
            await rkn_botz.register_user(user_id)
        except Exception:
            pass

        # If force sub not enabled
        if not self.channel:
            return False

        try:
            member = await client.get_chat_member(self.channel, user_id)

            # Block if user LEFT or is BANNED
            return member.status in (
                enums.ChatMemberStatus.LEFT,
                enums.ChatMemberStatus.BANNED
            )

        except UserNotParticipant:
            # Not joined → block
            return True

        except Exception:
            # Any unknown error → allow bot to continue
            return False


# ─────────────────────────────────────
# 📩 Handler for Unsubscribed Users
# ─────────────────────────────────────
@Client.on_message(
    filters.private &
    filters.create(
        ForceSubCheck(Rkn_Botz.FORCE_SUB),
        name="force_sub_check"
    )
)
async def handle_force_sub(client: Client, message: Message):
    user_id = message.from_user.id
    channel = Rkn_Botz.FORCE_SUB.lstrip("@")
    chat_link = f"https://t.me/{channel}"

    # Join button
    buttons = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🔔 Join Update Channel", url=chat_link)]]
    )

    # Check ban status
    try:
        member = await client.get_chat_member(channel, user_id)
        if member.status == enums.ChatMemberStatus.BANNED:
            return await message.reply_text(
                "**🚫 You are banned from using this bot.**\n"
                "Contact admin if you think this is a mistake."
            )
    except UserNotParticipant:
        pass
    except Exception:
        pass

    # Default force-sub message
    return await message.reply_text(
        "**🔐 To use this bot, you must join our update channel first.**\n\n"
        "👉 Click the button below and join, then come back.",
        reply_markup=buttons
    )