# =======================================================
#                    REQUIREMENTS.TXT
# =======================================================
"""
python-telegram-bot==20.7
pytz==2023.3
asyncio==3.4.3
"""

# =======================================================
#                    MAIN BOT CODE (bot.py)
# =======================================================

"""
# =======================================================
#                    CONFIGURATION
# =======================================================
TOKEN = "8960093466:AAH4dnaAZYaPteThN4rGjLk4EK-fg_4R2lI"
TOKENS = [TOKEN]

# Owner IDs
OWNER_IDS = [8785590284, 8505151232]

# =======================================================
#                    PREMIUM EMOJI MAP
# =======================================================
PREMIUM_EMOJIS = {
    "star": "⭐",
    "crown": "👑",
    "sparkle": "✨",
    "fire": "🔥",
    "gem": "💎",
    "rocket": "🚀",
    "rainbow": "🌈",
    "glow": "🌟",
    "lightning": "⚡",
    "gold": "🏆",
    "moon": "🌙",
    "sun": "☀️",
    "rose": "🌹",
    "diamond": "💠",
    "comet": "☄️",
    "galaxy": "🌌",
    "sparkles": "✧",
    "premium": "👾",
    "bling": "💫",
    "magic": "🪄",
    "lock": "🔒",
    "unlock": "🔓",
    "warning": "⚠️",
    "info": "ℹ️",
    "check": "✅",
    "cross": "❌",
    "muted": "🔇",
    "unmuted": "🔊",
    "kicked": "👢",
    "banned": "🚫",
    "promoted": "👑",
    "demoted": "⬇️",
    "welcome": "🎉",
    "party": "🎊",
    "heart": "❤️",
    "thumbsup": "👍",
    "clap": "👏",
    "handshake": "🤝",
    "smile": "😊",
    "flower": "🌸",
    "wave": "👋",
    "star2": "🌟",
    "confetti": "🎊"
}

# =======================================================
#                    GLOBAL STATE
# =======================================================
BOT_GLOBALLY_OFF = False
GC_LINKS = []  # Add your GC links here
folder_messages = {}

# =======================================================
#                    IMPORTS
# =======================================================
import logging
import asyncio
from datetime import datetime
import pytz

from telegram import Update, ChatPermissions
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Timezone
IST = pytz.timezone('Asia/Kolkata')

# =======================================================
#                    DECORATORS
# =======================================================
def owner_only(func):
    async def wrapper(update, context, *args, **kwargs):
        if update.effective_user.id not in OWNER_IDS:
            await update.message.reply_text(
                f"{PREMIUM_EMOJIS['warning']} **𝐎𝐧𝐥𝐲 𝐎𝐰𝐧𝐞𝐫 𝐂𝐚𝐧 𝐔𝐬𝐞 𝐓𝐡𝐢𝐬 𝐂𝐨𝐦𝐦𝐚𝐧𝐝!** {PREMIUM_EMOJIS['warning']}"
            )
            return
        return await func(update, context, *args, **kwargs)
    return wrapper

def admin_only(func):
    async def wrapper(update, context, *args, **kwargs):
        chat_id = update.effective_chat.id
        user_id = update.effective_user.id
        
        if user_id in OWNER_IDS:
            return await func(update, context, *args, **kwargs)
            
        try:
            member = await context.bot.get_chat_member(chat_id, user_id)
            if member.status not in ['administrator', 'creator']:
                await update.message.reply_text(
                    f"{PREMIUM_EMOJIS['warning']} **𝐀𝐝𝐦𝐢𝐧 𝐂𝐨𝐦𝐦𝐚𝐧𝐝 𝐎𝐧𝐥𝐲!** {PREMIUM_EMOJIS['warning']}"
                )
                return
        except Exception as e:
            await update.message.reply_text(
                f"{PREMIUM_EMOJIS['cross']} **𝐄𝐫𝐫𝐨𝐫: {str(e)}** {PREMIUM_EMOJIS['cross']}"
            )
            return
        return await func(update, context, *args, **kwargs)
    return wrapper

def sudo_only(func):
    async def wrapper(update, context, *args, **kwargs):
        if context.bot.token != TOKENS[0]:
            return
        return await func(update, context, *args, **kwargs)
    return wrapper

def check_bot_state(func):
    async def wrapper(update, context, *args, **kwargs):
        if BOT_GLOBALLY_OFF:
            await update.message.reply_text(
                f"{PREMIUM_EMOJIS['moon']} **𝐁𝐨𝐭 𝐢𝐬 𝐜𝐮𝐫𝐫𝐞𝐧𝐭𝐥𝐲 𝐎𝐅𝐅!** {PREMIUM_EMOJIS['moon']}"
            )
            return
        return await func(update, context, *args, **kwargs)
    return wrapper

# =======================================================
#                    START COMMAND
# =======================================================
@sudo_only
async def start(update, context):
    if context.bot.token != TOKENS[0]:
        return
    
    welcome_text = f"""
{PREMIUM_EMOJIS['star']}{PREMIUM_EMOJIS['crown']}{PREMIUM_EMOJIS['star']} **𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 𝐑𝐈𝐒𝐇𝐔 𝐆𝐀𝐋𝐀𝐗𝐘** {PREMIUM_EMOJIS['star']}{PREMIUM_EMOJIS['crown']}{PREMIUM_EMOJIS['star']}

{PREMIUM_EMOJIS['sparkle']}{PREMIUM_EMOJIS['fire']}{PREMIUM_EMOJIS['sparkle']} **𝐈'𝐦 𝐑ɪ𝐒ʜ𝐔 𝐆ᴀʟᴀxʏ 𝐁𝐨𝐭** {PREMIUM_EMOJIS['sparkle']}{PREMIUM_EMOJIS['fire']}{PREMIUM_EMOJIS['sparkle']}

{PREMIUM_EMOJIS['gem']} **𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐁𝐲:** 𝐅𝐞𝐚𝐫𝐎𝐟𝐑𝐢𝐬𝐡𝐮 {PREMIUM_EMOJIS['gem']}

{PREMIUM_EMOJIS['rocket']} **𝐁𝐨𝐭 𝐒𝐭𝐚𝐭𝐮𝐬:** {'🟢 𝐎𝐍' if not BOT_GLOBALLY_OFF else '🔴 𝐎𝐅𝐅'}

📋 **𝐆𝐑𝐎𝐔𝐏 𝐑𝐔𝐋𝐄𝐒:**
{PREMIUM_EMOJIS['fire']} 𝐍𝐨 𝐀𝐛𝐮𝐬𝐞
{PREMIUM_EMOJIS['fire']} 𝐍𝐨 𝐒𝐩𝐚𝐦
{PREMIUM_EMOJIS['fire']} 𝐍𝐨 𝐀𝐝𝐬
{PREMIUM_EMOJIS['fire']} 𝐍𝐨 𝐍𝐒𝐅𝐖
{PREMIUM_EMOJIS['fire']} 𝐍𝐨 𝐀𝐛𝐮𝐬𝐢𝐯𝐞 𝐋𝐚𝐧𝐠𝐮𝐚𝐠𝐞
{PREMIUM_EMOJIS['fire']} 𝐅𝐨𝐥𝐥𝐨𝐰 𝐀𝐝𝐦𝐢𝐧𝐬

{PREMIUM_EMOJIS['moon']} **𝐓𝐲𝐩𝐞** `/help` **𝐅𝐨𝐫 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬** {PREMIUM_EMOJIS['moon']}

{PREMIUM_EMOJIS['rose']}{PREMIUM_EMOJIS['gold']}{PREMIUM_EMOJIS['rose']} **𝐌𝐚𝐝𝐞 𝐖𝐢𝐭𝐡 ❤️ 𝐁𝐲 𝐑ɪ𝐒ʜ𝐔** {PREMIUM_EMOJIS['rose']}{PREMIUM_EMOJIS['gold']}{PREMIUM_EMOJIS['rose']}
"""
    await update.message.reply_text(welcome_text)

# =======================================================
#                    HELP COMMAND
# =======================================================
@sudo_only
async def help_command(update, context):
    if context.bot.token != TOKENS[0]:
        return
    
    help_text = f"""
{PREMIUM_EMOJIS['crown']} **𝐑ɪ𝐒ʜ𝐔 𝐆ᴀʟᴀxʏ 𝐁𝐨𝐭 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬** {PREMIUM_EMOJIS['crown']}

{PREMIUM_EMOJIS['sparkle']} **𝐀𝐝𝐦𝐢𝐧 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬:** {PREMIUM_EMOJIS['sparkle']}

{PREMIUM_EMOJIS['muted']} `/mute` - Mute a user (reply to user)
{PREMIUM_EMOJIS['unmuted']} `/unmute` - Unmute a user (reply to user)
{PREMIUM_EMOJIS['kicked']} `/kick` - Kick user from group (reply to user)
{PREMIUM_EMOJIS['banned']} `/ban` - Ban user from group (reply to user)
{PREMIUM_EMOJIS['check']} `/unban` - Unban user (reply to user)
{PREMIUM_EMOJIS['promoted']} `/promote` - Promote user to admin (reply to user)
{PREMIUM_EMOJIS['demoted']} `/demote` - Demote admin (reply to user)
{PREMIUM_EMOJIS['lock']} `/lock` - Lock group (only admins can send)
{PREMIUM_EMOJIS['unlock']} `/unlock` - Unlock group (everyone can send)

{PREMIUM_EMOJIS['crown']} **𝐎𝐰𝐧𝐞𝐫 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬:** {PREMIUM_EMOJIS['crown']}

{PREMIUM_EMOJIS['moon']} `/off` - Turn bot OFF globally
{PREMIUM_EMOJIS['sun']} `/on` - Turn bot ON globally
{PREMIUM_EMOJIS['galaxy']} `/gcs` - Show total GCs
{PREMIUM_EMOJIS['folder']} `/folder` - Show GC links
{PREMIUM_EMOJIS['unfolder']} `/unfolder` - Remove GC links

📋 **𝐆𝐑𝐎𝐔𝐏 𝐑𝐔𝐋𝐄𝐒:**
{PREMIUM_EMOJIS['fire']} 𝐍𝐨 𝐀𝐛𝐮𝐬𝐞
{PREMIUM_EMOJIS['fire']} 𝐍𝐨 𝐒𝐩𝐚𝐦
{PREMIUM_EMOJIS['fire']} 𝐍𝐨 𝐀𝐝𝐬
{PREMIUM_EMOJIS['fire']} 𝐍𝐨 𝐍𝐒𝐅𝐖
{PREMIUM_EMOJIS['fire']} 𝐅𝐨𝐥𝐥𝐨𝐰 𝐀𝐝𝐦𝐢𝐧𝐬

{PREMIUM_EMOJIS['rose']} **𝐌𝐚𝐝𝐞 𝐖𝐢𝐭𝐡 ❤️ 𝐁𝐲 𝐑ɪ𝐒ʜ𝐔** {PREMIUM_EMOJIS['rose']}
"""
    await update.message.reply_text(help_text)

# =======================================================
#                    WELCOME NEW MEMBER HANDLER
# =======================================================
@sudo_only
async def welcome_new_member(update, context):
    if context.bot.token != TOKENS[0] or BOT_GLOBALLY_OFF:
        return

    if not update.message or not update.message.new_chat_members:
        return

    chat_id = update.effective_chat.id
    group_name = update.effective_chat.title or "Group"
    
    msg_date = update.message.date.astimezone(IST)
    time_str = msg_date.strftime("%I:%M %p")
    date_str = msg_date.strftime("%d/%m/%Y")
    day_str = msg_date.strftime("%A")

    for new_member in update.message.new_chat_members:
        if new_member.id == context.bot.id:
            continue
            
        first_name = new_member.first_name or "User"
        username = f"@{new_member.username}" if new_member.username else "N/A"
        user_mention = f"[{first_name}](tg://user?id={new_member.id})"
        
        welcome_message = f"""
{PREMIUM_EMOJIS['welcome']}{PREMIUM_EMOJIS['party']}{PREMIUM_EMOJIS['welcome']} **𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 𝐑𝐈𝐒𝐇𝐔 𝐆𝐀𝐋𝐀𝐗𝐘** {PREMIUM_EMOJIS['welcome']}{PREMIUM_EMOJIS['party']}{PREMIUM_EMOJIS['welcome']}

{PREMIUM_EMOJIS['star']} **𝐖𝐞𝐥𝐜𝐨𝐦𝐞 {user_mention}** {PREMIUM_EMOJIS['star']}

{PREMIUM_EMOJIS['gem']} **𝐍𝐚𝐦𝐞:** {first_name} {PREMIUM_EMOJIS['gem']}
{PREMIUM_EMOJIS['glow']} **𝐔𝐬𝐞𝐫𝐧𝐚𝐦𝐞:** {username} {PREMIUM_EMOJIS['glow']}
{PREMIUM_EMOJIS['sun']} **𝐃𝐚𝐲:** {day_str} {PREMIUM_EMOJIS['sun']}
{PREMIUM_EMOJIS['moon']} **𝐓𝐢𝐦𝐞:** {time_str} {date_str} {PREMIUM_EMOJIS['moon']}
{PREMIUM_EMOJIS['galaxy']} **𝐆𝐫𝐨𝐮𝐩:** {group_name} {PREMIUM_EMOJIS['galaxy']}

{PREMIUM_EMOJIS['sparkle']} **𝐆𝐫𝐨𝐮𝐩 𝐑𝐮𝐥𝐞𝐬:** {PREMIUM_EMOJIS['sparkle']}
{PREMIUM_EMOJIS['fire']} • 𝐍𝐨 𝐀𝐛𝐮𝐬𝐞
{PREMIUM_EMOJIS['fire']} • 𝐍𝐨 𝐒𝐩𝐚𝐦
{PREMIUM_EMOJIS['fire']} • 𝐍𝐨 𝐀𝐝𝐬
{PREMIUM_EMOJIS['fire']} • 𝐍𝐨 𝐍𝐒𝐅𝐖
{PREMIUM_EMOJIS['fire']} • 𝐅𝐨𝐥𝐥𝐨𝐰 𝐀𝐝𝐦𝐢𝐧𝐬

{PREMIUM_EMOJIS['heart']} **𝐌𝐚𝐝𝐞 𝐖𝐢𝐭𝐡 ❤️ 𝐁𝐲 𝐑ɪ𝐒ʜ𝐔** {PREMIUM_EMOJIS['heart']}

{PREMIUM_EMOJIS['clap']} **𝐄𝐧𝐣𝐨𝐲 𝐘𝐨𝐮𝐫 𝐒𝐭𝐚𝐲!** {PREMIUM_EMOJIS['clap']}
"""
        
        try:
            await update.message.reply_text(
                welcome_message,
                parse_mode='Markdown',
                disable_web_page_preview=True
            )
        except Exception as e:
            logger.error(f"Failed to send welcome message: {e}")

# =======================================================
#                    GLOBAL ON/OFF COMMANDS (OWNER ONLY)
# =======================================================
@owner_only
@sudo_only
async def global_off(update, context):
    global BOT_GLOBALLY_OFF
    if context.bot.token != TOKENS[0]:
        return
    BOT_GLOBALLY_OFF = True
    await update.message.reply_text(
        f"{PREMIUM_EMOJIS['moon']} **𝐁𝐨𝐭 𝐓𝐮𝐫𝐧𝐞𝐝 𝐎𝐅𝐅 𝐆𝐥𝐨𝐛𝐚𝐥𝐥𝐲** {PREMIUM_EMOJIS['moon']}"
    )

@owner_only
@sudo_only
async def global_on(update, context):
    global BOT_GLOBALLY_OFF
    if context.bot.token != TOKENS[0]:
        return
    BOT_GLOBALLY_OFF = False
    await update.message.reply_text(
        f"{PREMIUM_EMOJIS['sun']} **𝐁𝐨𝐭 𝐓𝐮𝐫𝐧𝐞𝐝 𝐎𝐍 𝐆𝐥𝐨𝐛𝐚𝐥𝐥𝐲** {PREMIUM_EMOJIS['sun']}"
    )

# =======================================================
#                    MUTE COMMAND (ADMIN ONLY)
# =======================================================
@admin_only
@check_bot_state
@sudo_only
async def mute(update, context):
    if context.bot.token != TOKENS[0]:
        return
        
    if not update.message.reply_to_message:
        await update.message.reply_text(
            f"{PREMIUM_EMOJIS['warning']} **𝐏𝐥𝐞𝐚𝐬𝐞 𝐫𝐞𝐩𝐥𝐲 𝐭𝐨 𝐚 𝐮𝐬𝐞𝐫'𝐬 𝐦𝐞𝐬𝐬𝐚𝐠𝐞!** {PREMIUM_EMOJIS['warning']}"
        )
        return
        
    user = update.message.reply_to_message.from_user
    chat_id = update.effective_chat.id
    
    try:
        target_member = await context.bot.get_chat_member(chat_id, user.id)
        if target_member.status in ['administrator', 'creator']:
            await update.message.reply_text(
                f"{PREMIUM_EMOJIS['cross']} **𝐂𝐚𝐧𝐧𝐨𝐭 𝐦𝐮𝐭𝐞 𝐚𝐧 𝐚𝐝𝐦𝐢𝐧/𝐨𝐰𝐧𝐞𝐫!** {PREMIUM_EMOJIS['cross']}"
            )
            return
    except:
        pass
    
    try:
        await context.bot.restrict_chat_member(
            chat_id,
            user.id,
            permissions=ChatPermissions(can_send_messages=False)
        )
        await update.message.reply_text(
            f"{PREMIUM_EMOJIS['muted']} **🔇 {user.first_name} 𝐌𝐮𝐭𝐞𝐝 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲!** {PREMIUM_EMOJIS['muted']}"
        )
    except Exception as e:
        await update.message.reply_text(
            f"{PREMIUM_EMOJIS['cross']} **𝐅𝐚𝐢𝐥𝐞𝐝 𝐭𝐨 𝐦𝐮𝐭𝐞: {str(e)}** {PREMIUM_EMOJIS['cross']}"
        )

# =======================================================
#                    UNMUTE COMMAND (ADMIN ONLY)
# =======================================================
@admin_only
@check_bot_state
@sudo_only
async def unmute(update, context):
    if context.bot.token != TOKENS[0]:
        return
        
    if not update.message.reply_to_message:
        await update.message.reply_text(
            f"{PREMIUM_EMOJIS['warning']} **𝐏𝐥𝐞𝐚𝐬𝐞 𝐫𝐞𝐩𝐥𝐲 𝐭𝐨 𝐚 𝐮𝐬𝐞𝐫'𝐬 𝐦𝐞𝐬𝐬𝐚𝐠𝐞!** {PREMIUM_EMOJIS['warning']}"
        )
        return
        
    user = update.message.reply_to_message.from_user
    chat_id = update.effective_chat.id
    
    try:
        await context.bot.restrict_chat_member(
            chat_id,
            user.id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_send_polls=True,
                can_add_web_page_previews=True
            )
        )
        await update.message.reply_text(
            f"{PREMIUM_EMOJIS['unmuted']} **🔊 {user.first_name} 𝐔𝐧𝐦𝐮𝐭𝐞𝐝 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲!** {PREMIUM_EMOJIS['unmuted']}"
        )
    except Exception as e:
        await update.message.reply_text(
            f"{PREMIUM_EMOJIS['cross']} **𝐅𝐚𝐢𝐥𝐞𝐝 𝐭𝐨 𝐮𝐧𝐦𝐮𝐭𝐞: {str(e)}** {PREMIUM_EMOJIS['cross']}"
        )

# =======================================================
#                    KICK COMMAND (ADMIN ONLY)
# =======================================================
@admin_only
@check_bot_state
@sudo_only
async def kick(update, context):
    if context.bot.token != TOKENS[0]:
        return
        
    if not update.message.reply_to_message:
        await update.message.reply_text(
            f"{PREMIUM_EMOJIS['warning']} **𝐏𝐥𝐞𝐚𝐬𝐞 𝐫𝐞𝐩𝐥𝐲 𝐭𝐨 𝐚 𝐮𝐬𝐞𝐫'𝐬 𝐦𝐞𝐬𝐬𝐚𝐠𝐞!** {PREMIUM_EMOJIS['warning']}"
        )
        return
        
    user = update.message.reply_to_message.from_user
    chat_id = update.effective_chat.id
    
    try:
        target_member = await context.bot.get_chat_member(chat_id, user.id)
        if target_member.status in ['administrator', 'creator']:
            await update.message.reply_text(
                f"{PREMIUM_EMOJIS['cross']} **𝐂𝐚𝐧𝐧𝐨𝐭 𝐤𝐢𝐜𝐤 𝐚𝐧 𝐚𝐝𝐦𝐢𝐧/𝐨𝐰𝐧𝐞𝐫!** {PREMIUM_EMOJIS['cross']}"
            )
            return
    except:
        pass
    
    try:
        await context.bot.ban_chat_member(chat_id, user.id)
        await context.bot.unban_chat_member(chat_id, user.id)
        await update.message.reply_text(
            f"{PREMIUM_EMOJIS['kicked']} **👢 {user.first_name} 𝐊𝐢𝐜𝐤𝐞𝐝 𝐅𝐫𝐨𝐦 𝐆𝐫𝐨𝐮𝐩!** {PREMIUM_EMOJIS['kicked']}"
        )
    except Exception as e:
        await update.message.reply_text(
            f"{PREMIUM_EMOJIS['cross']} **𝐅𝐚𝐢𝐥𝐞𝐝 𝐭𝐨 𝐤𝐢𝐜𝐤: {str(e)}** {PREMIUM_EMOJIS['cross']}"
        )

# =======================================================
#                    BAN COMMAND (ADMIN ONLY)
# =======================================================
@admin_only
@check_bot_state
@sudo_only
async def ban(update, context):
    if context.bot.token != TOKENS[0]:
        return
        
    if not update.message.reply_to_message:
        await update.message.reply_text(
            f"{PREMIUM_EMOJIS['warning']} **𝐏𝐥𝐞𝐚𝐬𝐞 𝐫𝐞𝐩𝐥𝐲 𝐭𝐨 𝐚 𝐮𝐬𝐞𝐫'𝐬 𝐦𝐞𝐬𝐬𝐚𝐠𝐞!** {PREMIUM_EMOJIS['warning']}"
        )
        return
        
    user = update.message.reply_to_message.from_user
    chat_id = update.effective_chat.id
    
    try:
        target_member = await context.bot.get_chat_member(chat_id, user.id)
        if target_member.status in ['administrator', 'creator']:
            await update.message.reply_text(
                f"{PREMIUM_EMOJIS['cross']} **𝐂𝐚𝐧𝐧𝐨𝐭 𝐛𝐚𝐧 𝐚𝐧 𝐚𝐝𝐦𝐢𝐧/𝐨𝐰𝐧𝐞𝐫!** {PREMIUM_EMOJIS['cross']}"
            )
            return
    except:
        pass
    
    try:
        await context.bot.ban_chat_member(chat_id, user.id)
        await update.message.reply_text(
            f"{PREMIUM_EMOJIS['banned']} **🚫 {user.first_name} 𝐁𝐚𝐧𝐧𝐞𝐝 𝐅𝐫𝐨𝐦 𝐆𝐫𝐨𝐮𝐩!** {PREMIUM_EMOJIS['banned']}"
        )
    except Exception as e:
        await update.message.reply_text(
            f"{PREMIUM_EMOJIS['cross']} **𝐅𝐚𝐢𝐥𝐞𝐝 𝐭𝐨 𝐛𝐚𝐧: {str(e)}** {PREMIUM_EMOJIS['cross']}"
        )

# =======================================================
#                    UNBAN COMMAND (ADMIN ONLY)
# =======================================================
@admin_only
@check_bot_state
@sudo_only
async def unban(update, context):
    if context.bot.token != TOKENS[0]:
        return
        
    if not update.message.reply_to_message:
        await update.message.reply_text(
            f"{PREMIUM_EMOJIS['warning']} **𝐏𝐥𝐞𝐚𝐬𝐞 𝐫𝐞𝐩𝐥𝐲 𝐭𝐨 𝐚 𝐮𝐬𝐞𝐫'𝐬 𝐦𝐞𝐬𝐬𝐚𝐠𝐞!** {PREMIUM_EMOJIS['warning']}"
        )
        return
        
    user = update.message.reply_to_message.from_user
    chat_id = update.effective_chat.id
    
    try:
        await context.bot.unban_chat_member(chat_id, user.id)
        await update.message.reply_text(
            f"{PREMIUM_EMOJIS['check']} **✅ {user.first_name} 𝐔𝐧𝐛𝐚𝐧𝐧𝐞𝐝 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲!** {PREMIUM_EMOJIS['check']}"
        )
    except Exception as e:
        await update.message.reply_text(
            f"{PREMIUM_EMOJIS['cross']} **𝐅𝐚𝐢𝐥𝐞𝐝 𝐭𝐨 𝐮𝐧𝐛𝐚𝐧: {str(e)}** {PREMIUM_EMOJIS['cross']}"
        )

# =======================================================
#                    PROMOTE COMMAND (ADMIN ONLY)
# =======================================================
@admin_only
@check_bot_state
@sudo_only
async def promote(update, context):
    if context.bot.token != TOKENS[0]:
        return
        
    if not update.message.reply_to_message:
        await update.message.reply_text(
            f"{PREMIUM_EMOJIS['warning']} **𝐏𝐥𝐞𝐚𝐬𝐞 𝐫𝐞𝐩𝐥𝐲 𝐭𝐨 𝐚 𝐮𝐬𝐞𝐫'𝐬 𝐦𝐞𝐬𝐬𝐚𝐠𝐞!** {PREMIUM_EMOJIS['warning']}"
        )
        return
        
    user = update.message.reply_to_message.from_user
    chat_id = update.effective_chat.id
    
    if user.id in OWNER_IDS:
        await update.message.reply_text(
            f"{PREMIUM_EMOJIS['cross']} **𝐂𝐚𝐧𝐧𝐨𝐭 𝐩𝐫𝐨𝐦𝐨𝐭𝐞 𝐚𝐧 𝐨𝐰𝐧𝐞𝐫!** {PREMIUM_EMOJIS['cross']}"
        )
        return
    
    try:
        await context.bot.promote_chat_member(
            chat_id,
            user.id,
            can_change_info=True,
            can_invite_users=True,
            can_pin_messages=True,
            can_manage_chat=True,
            can_delete_messages=True,
            can_restrict_members=True,
            can_promote_members=False
        )
        await update.message.reply_text(
            f"{PREMIUM_EMOJIS['promoted']} **👑 {user.first_name} 𝐏𝐫𝐨𝐦𝐨𝐭𝐞𝐝 𝐭𝐨 𝐀𝐝𝐦𝐢𝐧!** {PREMIUM_EMOJIS['promoted']}"
        )
    except Exception as e:
        await update.message.reply_text(
            f"{PREMIUM_EMOJIS['cross']} **𝐅𝐚𝐢𝐥𝐞𝐝 𝐭𝐨 𝐩𝐫𝐨𝐦𝐨𝐭𝐞: {str(e)}** {PREMIUM_EMOJIS['cross']}"
        )

# =======================================================
#                    DEMOTE COMMAND (ADMIN ONLY)
# =======================================================
@admin_only
@check_bot_state
@sudo_only
async def demote(update, context):
    if context.bot.token != TOKENS[0]:
        return
        
    if not update.message.reply_to_message:
        await update.message.reply_text(
            f"{PREMIUM_EMOJIS['warning']} **𝐏𝐥𝐞𝐚𝐬𝐞 𝐫𝐞𝐩𝐥𝐲 𝐭𝐨 𝐚 𝐮𝐬𝐞𝐫'𝐬 𝐦𝐞𝐬𝐬𝐚𝐠𝐞!** {PREMIUM_EMOJIS['warning']}"
        )
        return
        
    user = update.message.reply_to_message.from_user
    chat_id = update.effective_chat.id
    
    if user.id in OWNER_IDS:
        await update.message.reply_text(
            f"{PREMIUM_EMOJIS['cross']} **𝐂𝐚𝐧𝐧𝐨𝐭 𝐝𝐞𝐦𝐨𝐭𝐞 𝐚𝐧 𝐨𝐰𝐧𝐞𝐫!** {PREMIUM_EMOJIS['cross']}"
        )
        return
    
    try:
        await context.bot.promote_chat_member(
            chat_id,
            user.id,
            can_change_info=False,
            can_invite_users=False,
            can_pin_messages=False,
            can_manage_chat=False,
            can_delete_messages=False,
            can_restrict_members=False,
            can_promote_members=False
        )
        await update.message.reply_text(
            f"{PREMIUM_EMOJIS['demoted']} **⬇️ {user.first_name} 𝐃𝐞𝐦𝐨𝐭𝐞𝐝 𝐅𝐫𝐨𝐦 𝐀𝐝𝐦𝐢𝐧!** {PREMIUM_EMOJIS['demoted']}"
        )
    except Exception as e:
        await update.message.reply_text(
            f"{PREMIUM_EMOJIS['cross']} **𝐅𝐚𝐢𝐥𝐞𝐝 𝐭𝐨 𝐝𝐞𝐦𝐨𝐭𝐞: {str(e)}** {PREMIUM_EMOJIS['cross']}"
        )

# =======================================================
#                    LOCK GROUP (ADMIN ONLY)
# =======================================================
@admin_only
@check_bot_state
@sudo_only
async def lock_group(update, context):
    if context.bot.token != TOKENS[0]:
        return
        
    chat_id = update.effective_chat.id
    
    try:
        await context.bot.set_chat_permissions(
            chat_id,
            ChatPermissions(
                can_send_messages=False,
                can_send_media_messages=False,
                can_send_other_messages=False,
                can_send_polls=False,
                can_add_web_page_previews=False
            )
        )
        await update.message.reply_text(
            f"{PREMIUM_EMOJIS['lock']} **🔒 𝐆𝐫𝐨𝐮𝐩 𝐋𝐨𝐜𝐤𝐞𝐝!** {PREMIUM_EMOJIS['lock']}\n"
            f"{PREMIUM_EMOJIS['info']} **𝐎𝐧𝐥𝐲 𝐀𝐝𝐦𝐢𝐧𝐬 & 𝐎𝐰𝐧𝐞𝐫 𝐜𝐚𝐧 𝐬𝐞𝐧𝐝 𝐦𝐞𝐬𝐬𝐚𝐠𝐞𝐬** {PREMIUM_EMOJIS['info']}"
        )
    except Exception as e:
        await update.message.reply_text(
            f"{PREMIUM_EMOJIS['cross']} **𝐅𝐚𝐢𝐥𝐞𝐝 𝐭𝐨 𝐥𝐨𝐜𝐤: {str(e)}** {PREMIUM_EMOJIS['cross']}"
        )

# =======================================================
#                    UNLOCK GROUP (ADMIN ONLY)
# =======================================================
@admin_only
@check_bot_state
@sudo_only
async def unlock_group(update, context):
    if context.bot.token != TOKENS[0]:
        return
        
    chat_id = update.effective_chat.id
    
    try:
        await context.bot.set_chat_permissions(
            chat_id,
            ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_send_polls=True,
                can_add_web_page_previews=True,
                can_change_info=False,
                can_invite_users=True,
                can_pin_messages=False
            )
        )
        await update.message.reply_text(
            f"{PREMIUM_EMOJIS['unlock']} **🔓 𝐆𝐫𝐨𝐮𝐩 𝐔𝐧𝐥𝐨𝐜𝐤𝐞𝐝!** {PREMIUM_EMOJIS['unlock']}\n"
            f"{PREMIUM_EMOJIS['info']} **𝐄𝐯𝐞𝐫𝐲𝐨𝐧𝐞 𝐜𝐚𝐧 𝐧𝐨𝐰 𝐬𝐞𝐧𝐝 𝐦𝐞𝐬𝐬𝐚𝐠𝐞𝐬** {PREMIUM_EMOJIS['info']}"
        )
    except Exception as e:
        await update.message.reply_text(
            f"{PREMIUM_EMOJIS['cross']} **𝐅𝐚𝐢𝐥𝐞𝐝 𝐭𝐨 𝐮𝐧𝐥𝐨𝐜𝐤: {str(e)}** {PREMIUM_EMOJIS['cross']}"
        )

# =======================================================
#                    GC COMMANDS (SUDO ONLY)
# =======================================================
@sudo_only
@check_bot_state
async def gcs(update, context):
    if context.bot.token != TOKENS[0]:
        return
    total = len(GC_LINKS)
    await update.message.reply_text(
        f"{PREMIUM_EMOJIS['galaxy']} **𝐓𝐨𝐭𝐚𝐥 𝐆𝐂𝐬 ~ {total}** {PREMIUM_EMOJIS['galaxy']}"
    )

@sudo_only
@check_bot_state
async def folder(update, context):
    if context.bot.token != TOKENS[0]:
        return
    chat_id = update.effective_chat.id
    sent_msgs = []
    for link in GC_LINKS:
        msg = await update.message.reply_text(
            f"{PREMIUM_EMOJIS['gem']} **𝐆𝐂 ~** {link} {PREMIUM_EMOJIS['gem']}",
            disable_web_page_preview=True
        )
        sent_msgs.append(msg.message_id)
        await asyncio.sleep(0.5)
    folder_messages[chat_id] = sent_msgs

@sudo_only
@check_bot_state
async def unfolder(update, context):
    if context.bot.token != TOKENS[0]:
        return
    chat_id = update.effective_chat.id
    if chat_id not in folder_messages:
        return await update.message.reply_text(
            f"{PREMIUM_EMOJIS['warning']} **𝐋𝐢𝐧𝐤𝐬 𝐀𝐥𝐫𝐞𝐚𝐝𝐲 𝐎𝐟𝐟 ~** {PREMIUM_EMOJIS['warning']}"
        )
    for msg_id in folder_messages[chat_id]:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
        except:
            pass
    del folder_messages[chat_id]
    await update.message.reply_text(
        f"{PREMIUM_EMOJIS['check']} **𝐋𝐢𝐧𝐤𝐬 𝐃𝐞𝐥𝐞𝐭𝐞𝐝 ~** {PREMIUM_EMOJIS['check']}"
    )

# =======================================================
#                    LEFT MEMBER HANDLER
# =======================================================
@sudo_only
async def left_member_handler(update, context):
    if context.bot.token != TOKENS[0] or BOT_GLOBALLY_OFF:
        return

    if not update.message or not update.message.left_chat_member:
        return

    chat_id = update.effective_chat.id
    group_name = update.effective_chat.title or "Group"
    user = update.message.left_chat_member
    
    first_name = user.first_name if user.first_name else "User"
    username = f"@{user.username}" if user.username else "N/A"
  
    msg_date = update.message.date.astimezone(IST)
    time_str = msg_date.strftime("%I:%M %p")
    date_str = msg_date.strftime("%d/%m/%Y")
    day_str = msg_date.strftime("%A")

    leave_msg_text = (
        f"╔═════════════════╗\n"
        f"{PREMIUM_EMOJIS['galaxy']}{PREMIUM_EMOJIS['sparkle']}{PREMIUM_EMOJIS['galaxy']}                              {PREMIUM_EMOJIS['galaxy']}{PREMIUM_EMOJIS['sparkle']}{PREMIUM_EMOJIS['galaxy']}\n"
        f"‎           {PREMIUM_EMOJIS['crown']} 𝐑ɪ𝐒ʜ𝐔 !! 𝐆ᴀʟᴀxʏ {PREMIUM_EMOJIS['crown']}\n"
        f"‎                             \n"
        f"╚═════════════════╝\n"
        f"{PREMIUM_EMOJIS['gem']} 𝐓ɪᴍᴇ: {time_str} {date_str} {PREMIUM_EMOJIS['gem']}\n"
        f"{PREMIUM_EMOJIS['sun']} 𝐃ᴀʏ: {day_str} {PREMIUM_EMOJIS['sun']}\n"
        f"{PREMIUM_EMOJIS['fire']} 𝐍ᴀᴍᴇ: {first_name} {PREMIUM_EMOJIS['fire']}\n"
        f"{PREMIUM_EMOJIS['glow']} 𝐔sᴇʀɴᴀᴍᴇ: {username} {PREMIUM_EMOJIS['glow']}\n"
        f"{PREMIUM_EMOJIS['star']} 𝐆ʀᴏᴜᴘ: {group_name} {PREMIUM_EMOJIS['star']}\n"
        f"╔═════════════════╗\n\n"
        f"             {PREMIUM_EMOJIS['rocket']} 𝐅ᴇᴀʀ𝐎ғ𝐑ɪ𝐒ʜ𝐔 {PREMIUM_EMOJIS['rocket']}\n\n"
        f"‎╚═════════════════╝"
    )

    try:
        sent_msg = await update.message.reply_text(leave_msg_text)
        await context.bot.pin_chat_message(
            chat_id=chat_id,
            message_id=sent_msg.message_id,
            disable_notification=True
        )
    except Exception:
        pass

# =======================================================
#                    ERROR HANDLER
# =======================================================
async def error_handler(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

# =======================================================
#                    MAIN FUNCTION
# =======================================================
def main():
    application = Application.builder().token(TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("mute", mute))
    application.add_handler(CommandHandler("unmute", unmute))
    application.add_handler(CommandHandler("kick", kick))
    application.add_handler(CommandHandler("ban", ban))
    application.add_handler(CommandHandler("unban", unban))
    application.add_handler(CommandHandler("promote", promote))
    application.add_handler(CommandHandler("demote", demote))
    application.add_handler(CommandHandler("lock", lock_group))
    application.add_handler(CommandHandler("unlock", unlock_group))
    application.add_handler(CommandHandler("gcs", gcs))
    application.add_handler(CommandHandler("folder", folder))
    application.add_handler(CommandHandler("unfolder", unfolder))
    application.add_handler(CommandHandler("off", global_off))
    application.add_handler(CommandHandler("on", global_on))

    # Message handlers
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))
    application.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, left_member_handler))

    # Error handler
    application.add_error_handler(error_handler)

    print(f"{PREMIUM_EMOJIS['rocket']} Bot is starting...")
    print(f"{PREMIUM_EMOJIS['crown']} Owner IDs: {OWNER_IDS}")
    print(f"{PREMIUM_EMOJIS['check']} Bot token: {TOKEN[:10]}...")
    print(f"{PREMIUM_EMOJIS['sparkle']} All features are active!")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
"""

# =======================================================
#                    HOW TO RUN
# =======================================================
"""
1. Save the code as bot.py
2. Create requirements.txt with:
   python-telegram-bot==20.7
   pytz==2023.3
   asyncio==3.4.3
3. Install requirements: pip install -r requirements.txt
4. Run: python bot.py
"""

# =======================================================
#                    SINGLE FILE DOWNLOAD
# =======================================================
# Copy the entire code above and save as bot.py
# All packages are included in the code
