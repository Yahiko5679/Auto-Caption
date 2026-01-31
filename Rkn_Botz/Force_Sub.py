from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.errors import UserNotParticipant

from config import Rkn_Botz
from .database import rkn_botz


# ─────────────────────────────────────
# 🔐 Force Subscribe Filter
# ─────────────────────────────────────
class ForceSubCheck:
    def __init__(self, channel: str):
        self.channel = channel.lstrip("@") if isinstance(channel, str) else None

        admins = Rkn_Botz.ADMIN
        self.admins = admins if isinstance(admins, list) else [admins]

    async def __call__(self, client: Client, message: Message) -> bool:
        if not message.from_user:
            return False  # ignore service msgs

        user_id = message.from_user.id

        # 🔹 Register user (safe)
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

            # ❌ Must join → handler should run
            if member.status in (
                enums.ChatMemberStatus.LEFT,
                enums.ChatMemberStatus.BANNED
            ):
                return True

            # ✅ Already joined → skip handler
            return False

        except UserNotParticipant:
            # ❌ Not joined → handler should run
            return True

        except Exception:
            # Fail-open (never block bot)
            return False


# ─────────────────────────────────────
# 📩 Force-Sub Message Handler
# ─────────────────────────────────────
@Client.on_message(
    filters.private &
    filters.create(
        ForceSubCheck(Rkn_Botz.FORCE_SUB),
        name="force_sub_check"
    )
)
async def handle_force_sub(client: Client, message: Message):
    channel = Rkn_Botz.FORCE_SUB.lstrip("@")
    chat_link = f"https://t.me/{channel}"

    buttons = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🔔 Join Update Channel", url=chat_link)]]
    )

    return await message.reply_text(
        "**🔐 To use this bot, you must join our update channel first.**\n\n"
        "👉 Join the channel and then send your file again.",
        reply_markup=buttons
    )