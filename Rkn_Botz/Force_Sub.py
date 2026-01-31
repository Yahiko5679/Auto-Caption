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
        self.channel = channel.lstrip("@") if isinstance(channel, str) else channel

        # Normalize admins once
        admins = Rkn_Botz.ADMIN
        self.admins = admins if isinstance(admins, list) else [admins]

    async def __call__(self, client: Client, message: Message) -> bool:
        if not message.from_user:
            return False

        user_id = message.from_user.id

        # 🔹 Register user safely
        try:
            await rkn_botz.register_user(user_id)
        except Exception:
            pass

        # 🔹 Force sub disabled
        if not self.channel:
            return False

        # 🔹 Skip OWNER & ADMINS
        if user_id == Rkn_Botz.OWNER_ID or user_id in self.admins:
            return False

        try:
            member = await client.get_chat_member(self.channel, user_id)

            # ✅ These users are ALLOWED
            if member.status in (
                enums.ChatMemberStatus.MEMBER,
                enums.ChatMemberStatus.ADMINISTRATOR,
                enums.ChatMemberStatus.OWNER
            ):
                return False

            # ❌ These users must JOIN
            if member.status in (
                enums.ChatMemberStatus.LEFT,
                enums.ChatMemberStatus.BANNED
            ):
                return True

            # Any other status → allow
            return False

        except Exception:
            # Fail-open: never block bot on API errors
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