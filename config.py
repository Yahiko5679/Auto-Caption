# AutoCaptionBot by RknDeveloper
# Copyright (c) 2024 RknDeveloper
# Licensed under the MIT License
# https://github.com/RknDeveloper/Rkn-AutoCaptionBot/blob/main/LICENSE
# Please retain this credit when using or forking this code.

# Developer Contacts:
# Telegram: @RknDeveloperr
# Updates Channel: @Rkn_Bots_Updates & @Rkn_Botz
# Special Thanks To: @ReshamOwner
# Update Channels: @Digital_Botz & @DigitalBotz_Support

# ⚠️ Please do not remove this credit!


import os
import time

class Rkn_Botz(object):
    # Rkn client config (required)
    API_ID = os.environ.get("API_ID", "")
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

    # Start pic (default image link)
    RKN_PIC = os.environ.get("RKN_PIC", "https://graph.org/file/fc40b362f9160e52b1ac8-76d6e6d95e9e27dad0.jpg")

    # Bot uptime (start time)
    BOT_UPTIME = time.time()

    # Server port (default 8080)
    PORT = int(os.environ.get("PORT", "8080"))

    # Force subscribe channel username (without @) (only public chats username required)
    FORCE_SUB = os.environ.get("FORCE_SUB", "MythicBots")

    # Database config (required)
    DB_NAME = os.environ.get("DB_NAME", "")
    DB_URL = os.environ.get("DB_URL", "")

    # Default caption (with safe fallback)
    DEFAULT_CAPTION = os.environ.get(
        "DEFAULT_CAPTION",
        "<b><a href='https://t.me/New_Anime_Hindi_Dub_Series'>{file_name} Main Telegram Channel: @New_Anime_Hindi_Dub_Series</a></b>"
    )

    # Sticker ID default
    STICKER_ID = os.environ.get(
        "STICKER_ID",
        "CAACAgIAAxkBAAELFqBllhB70i13m-woXeIWDXU6BD2j7wAC9gcAAkb7rAR7xdjVOS5ziTQE"
    )

    # Admin ID (single integer)
    ADMIN = list(map(int, os.environ.get("ADMIN", "6617544956").split()))  # Yahan default ko apne Telegram User ID se replace karo

# ————
# End of file
# Original author: @RknDeveloperr
# GitHub: https://github.com/RknDeveloper

# Developer Contacts:
# Telegram: @RknDeveloperr
# Updates Channel: @Rkn_Bots_Updates & @Rkn_Botz
# Special Thanks To: @ReshamOwner
# Update Channels: @Digital_Botz & @DigitalBotz_Support

# ⚠️ Please do not remove this credit!



class MythicBotz:
    HELP_TEXT = """
🆘 <b>Auto Caption Bot – Help</b>

<b>📤 How to Use</b>
• Send any video or document  
• Bot will auto-generate caption  
• Works best in private chat  

<b>🧩 Available Variables</b>
You can use these in caption formats 👇

• <code>{episode}</code> – Episode number  
• <code>{season}</code> – Season number  
• <code>{quality}</code> – Video quality (720p, 1080p, etc.)  
• <code>{year}</code> – Release year  
• <code>{language}</code> – Audio language  
• <code>{file_name}</code> – Original file name  
• <code>{caption}</code> – Original caption text  
• <code>{file_size}</code> – Media file size  
• <code>{description}</code> – Custom description  

<b>📝 Example Caption</b>
<blockquote>
🎬 {file_name}  
━━━━━━━━━━━━━━  
📺 Season: {season} | Ep: {episode}  
🎧 Language: {language}  
📀 Quality: {quality}  
📅 Year: {year}  
💾 Size: {file_size}  
━━━━━━━━━━━━━━  
{description}
</blockquote>

<b>⚙ Notes</b>
• HTML tags are supported  
• Variables auto-fill if available  
• Missing data will be skipped  

📌 Tip: Just upload & relax 😌
"""