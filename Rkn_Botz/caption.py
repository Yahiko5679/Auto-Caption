from pyrogram import Client, filters, errors, types
from config import Rkn_Botz, MythicBotz 
from .database import rkn_botz
import asyncio, time, re, os, sys


# =========================
# 👮 ADMIN COMMANDS
# =========================

@Client.on_message(filters.private & filters.user(Rkn_Botz.ADMIN) & filters.command(["users", "status"]))
async def show_user_stats(client, message):
    start = time.monotonic()
    rkn = await message.reply_text("🔍 Gathering bot statistics...")

    total = await rkn_botz.fetch_total_users()
    uptime = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - client.uptime))
    ping = (time.monotonic() - start) * 1000

    await rkn.edit_text(
        f"📊 <b>Bot Stats</b>\n\n"
        f"⏱️ <b>Uptime:</b> {uptime}\n"
        f"📡 <b>Ping:</b> <code>{ping:.2f} ms</code>\n"
        f"👤 <b>Total Users:</b> <code>{total}</code>"
    )


@Client.on_message(filters.private & filters.user(Rkn_Botz.ADMIN) & filters.command(["broadcast"]))
async def broadcast(client, message):
    if not message.reply_to_message:
        return await message.reply("❗ <b>Reply to a message to broadcast.</b>")

    status = await message.reply("🔄 Broadcasting...")

    users = await rkn_botz.list_all_users()
    success = failed = blocked = deactivated = 0

    for uid in users:
        try:
            await asyncio.sleep(0.5)
            await message.reply_to_message.copy(uid)
            success += 1
        except errors.InputUserDeactivated:
            deactivated += 1
            await rkn_botz.remove_user_by_id(uid)
        except errors.UserIsBlocked:
            blocked += 1
            await rkn_botz.remove_user_by_id(uid)
        except errors.FloodWait as e:
            await asyncio.sleep(e.value)
        except Exception:
            failed += 1

    await status.edit(
        f"<b>✅ Broadcast Completed</b>\n\n"
        f"👥 Total: {len(users)}\n"
        f"✅ Success: {success}\n"
        f"⛔ Blocked: {blocked}\n"
        f"🗑️ Deleted: {deactivated}\n"
        f"⚠️ Failed: {failed}"
    )


@Client.on_message(filters.private & filters.user(Rkn_Botz.ADMIN) & filters.command("restart"))
async def restart_bot(client, message):
    await message.reply("🔄 Restarting...")
    await asyncio.sleep(2)
    os.execl(sys.executable, sys.executable, *sys.argv)


# =========================
# 🚀 START
# =========================

@Client.on_message(filters.private & filters.command("start"))
async def start_cmd(client, message):
    await rkn_botz.register_user(message.from_user.id)

    await message.reply_photo(
        photo=Rkn_Botz.RKN_PIC,
        caption=(
            f"<b>Hey {message.from_user.mention} 👋\n\n"
            f"I'm an Auto Caption Bot.\n"
            f"I auto-edit captions for media posted in channels."
            f"<code>/set_caption</code> – Set your custom caption
<code>/delcaption</code> – Delete and use default caption"
            f"Note: Commands only work in channels where I'm admin."

            f"<blockquote>‣ ᴍᴀɪɴᴛᴀɪɴᴇᴅ ʙʏ : <a herf="https://t.me/VoidXTora">ᴘʀɪʏᴀɴꜱʜᴜ</a></blockquote></b>"
        ),
        reply_markup=types.InlineKeyboardMarkup(
            [
                # 🔝 Top row: Add me in channel
                [
                    types.InlineKeyboardButton(
                        "⇆ ᴀᴅᴅ ᴍᴇ ɪɴ ᴄʜᴀɴɴᴇʟ ⇆",
                        url=f"https://t.me/{MythicBotz.BOT_USERNAME}?startchannel=true"
                    )
                ],
                # 2nd row: Main channel + Help group
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
                # 3rd row: Source code
                [
                    types.InlineKeyboardButton(
                        "Source Code 🔥",
                        url="https://t.me/VoidXTora"
                    )
                ]
            ]
        )
    )


# =========================
# 📝 CHANNEL CAPTION SETUP
# =========================

@Client.on_message(filters.command(["set_caption", "setcap"]) & filters.channel)
async def set_caption(client, message):
    if len(message.command) < 2:
        return await message.reply("Usage: /set_caption <caption>")

    caption = message.text.split(" ", 1)[1]
    cid = message.chat.id

    data = await rkn_botz._channels_collection.find_one({"channelId": cid})
    if data:
        await rkn_botz.update_channel_caption(cid, caption)
    else:
        await rkn_botz.add_channel_caption(cid, caption)

    await message.reply("✅ Caption updated.")


@Client.on_message(filters.command(["delcaption", "delcap"]) & filters.channel)
async def del_caption(client, message):
    cid = message.chat.id
    await rkn_botz._channels_collection.delete_one({"channelId": cid})
    await message.reply("🗑️ Caption deleted.")


# =========================
# 🔍 EXTRACTION HELPERS
# =========================

def _two(num):
    try:
        return f"{int(num):02d}"
    except:
        return "Unknown"


def detect_season(text):
    if not text:
        return "Unknown"
    m = re.search(r'\bS(?:eason)?[\s\-_:]*(\d{1,2})\b', text, re.I)
    return _two(m.group(1)) if m else "Unknown"


def detect_episode(text):
    if not text:
        return "Unknown"
    m = re.search(r'\bE(?:p|pisode)?[\s\-_:]*(\d{1,4})\b', text, re.I)
    if m:
        ep = m.group(1)
        if len(ep) == 4 and ep.startswith(("19", "20")):
            return "Unknown"
        return _two(ep)
    return "Unknown"


def detect_year(text):
    m = re.search(r'\b(19\d{2}|20\d{2})\b', text or "")
    return m.group(1) if m else "Unknown"


def detect_quality(text):
    m = re.search(r'\b(2160p|1440p|1080p|720p|480p)\b', text or "", re.I)
    return m.group(1) if m else "Unknown"


def detect_language(text):
    langs = ['hindi','english','tamil','telugu','malayalam','kannada','bengali','marathi','urdu']
    found = [l.capitalize() for l in langs if re.search(rf'\b{l}\b', text or "", re.I)]
    return ", ".join(found) if found else "Unknown"


def detect_title(text):
    if not text:
        return "Unknown"

    t = re.sub(r'@\w+', '', text)
    t = re.sub(r'\bS(?:eason)?\s*\d+|\bE(?:p|pisode)?\s*\d+', '', t, flags=re.I)
    t = re.sub(r'\b(19\d{2}|20\d{2})\b', '', t)
    t = re.sub(r'\b(2160p|1440p|1080p|720p|x264|x265|10bit|web\-dl|multi|audio|esub)\b', '', t, flags=re.I)
    t = re.sub(r'[._\-]+', ' ', t)
    t = re.sub(r'\s{2,}', ' ', t).strip()

    return t if len(t) > 2 else "Unknown"


def convert_size(size):
    if not size:
        return "Unknown"
    for unit in ['B','KB','MB','GB','TB']:
        if size < 1024:
            return f"{round(size,2)} {unit}"
        size /= 1024


# =========================
# 🎬 AUTO CAPTION
# =========================

@Client.on_message(filters.channel)
async def auto_caption(client, message):
    if not message.media:
        return

    media = None
    for t in ("video", "audio", "document"):
        media = getattr(message, t, None)
        if media:
            break

    if not media or not media.file_name:
        return

    file_name = media.file_name.replace("_", " ")
    caption = message.caption or ""

    season = detect_season(file_name) or detect_season(caption)
    episode = detect_episode(file_name) or detect_episode(caption)

    if season == "Unknown":
        season = detect_season(caption)

    if episode == "Unknown":
        episode = detect_episode(caption)

    title = detect_title(file_name)
    if title == "Unknown":
        title = detect_title(caption)

    data = await rkn_botz._channels_collection.find_one({"channelId": message.chat.id})

    text = (data.get("caption") if data else Rkn_Botz.DEFAULT_CAPTION).format(
        title=title,
        file_name=file_name,
        caption=caption,
        season=season,
        episode=episode,
        year=detect_year(caption),
        quality=detect_quality(caption),
        language=detect_language(caption),
        file_size=convert_size(media.file_size)
    )

    try:
        await message.edit_caption(text)
    except errors.FloodWait as e:
        await asyncio.sleep(e.value)