# =======================================================
#                    CONFIGURATION
# =======================================================
TOKEN = "8960093466:AAH4dnaAZYaPteThN4rGjLk4EK-fg_4R2lI"
OWNER_IDS = [8785590284, 8505151232]

# =======================================================
#                    PREMIUM EMOJI MAP
# =======================================================
PREMIUM_EMOJIS = {
    "star": "⭐", "crown": "👑", "sparkle": "✨", "fire": "🔥",
    "gem": "💎", "rocket": "🚀", "rainbow": "🌈", "glow": "🌟",
    "lightning": "⚡", "gold": "🏆", "moon": "🌙", "sun": "☀️",
    "rose": "🌹", "diamond": "💠", "comet": "☄️", "galaxy": "🌌",
    "lock": "🔒", "unlock": "🔓", "warning": "⚠️", "info": "ℹ️",
    "check": "✅", "cross": "❌", "muted": "🔇", "unmuted": "🔊",
    "kicked": "👢", "banned": "🚫", "promoted": "👑", "demoted": "⬇️",
    "welcome": "🎉", "party": "🎊", "heart": "❤️", "thumbsup": "👍",
    "clap": "👏", "handshake": "🤝", "smile": "😊", "flower": "🌸",
    "wave": "👋", "star2": "🌟", "confetti": "🎊", "sparkles": "✧",
    "premium": "👾", "bling": "💫", "magic": "🪄"
}

# =======================================================
#                    GLOBAL STATE
# =======================================================
BOT_GLOBALLY_OFF = False
GC_LINKS = []
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

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)
IST = pytz.timezone('Asia/Kolkata')

# =======================================================
#                    DECORATORS - FIXED
# =======================================================
def owner_only(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        if update.effective_user.id not in OWNER_IDS:
            await update.message.reply_text(
                f"{PREMIUM_EMOJIS['warning']} **Only Owner Can Use This Command!**"
            )
            return
        return await func(update, context, *args, **kwargs)
    return wrapper

def admin_only(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        chat_id = update.effective_chat.id
        user_id = update.effective_user.id
        
        if user_id in OWNER_IDS:
            return await func(update, context, *args, **kwargs)
            
        try:
            member = await context.bot.get_chat_member(chat_id, user_id)
            if member.status not in ['administrator', 'creator']:
                await update.message.reply_text(
                    f"{PREMIUM_EMOJIS['warning']} **Admin Command Only!**"
                )
                return
        except Exception as e:
            await update.message.reply_text(
                f"{PREMIUM_EMOJIS['cross']} **Error: {str(e)}**"
            )
            return
        return await func(update, context, *args, **kwargs)
    return wrapper

def check_bot_state(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        if BOT_GLOBALLY_OFF:
            await update.message.reply_text(
                f"{PREMIUM_EMOJIS['moon']} **Bot is currently OFF!**"
            )
            return
        return await func(update, context, *args, **kwargs)
    return wrapper

# =======================================================
#                    START COMMAND
# =======================================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"""
{PREMIUM_EMOJIS['star']}{PREMIUM_EMOJIS['crown']}{PREMIUM_EMOJIS['star']} **WELCOME TO RISHU GALAXY** {PREMIUM_EMOJIS['star']}{PREMIUM_EMOJIS['crown']}{PREMIUM_EMOJIS['star']}

{PREMIUM_EMOJIS['sparkle']}{PREMIUM_EMOJIS['fire']}{PREMIUM_EMOJIS['sparkle']} **I'm Rishu Galaxy Bot** {PREMIUM_EMOJIS['sparkle']}{PREMIUM_EMOJIS['fire']}{PREMIUM_EMOJIS['sparkle']}

{PREMIUM_EMOJIS['gem']} **Powered By:** FearOfRishu {PREMIUM_EMOJIS['gem']}

{PREMIUM_EMOJIS['rocket']} **Bot Status:** {'🟢 ON' if not BOT_GLOBALLY_OFF else '🔴 OFF'}

📋 **GROUP RULES:**
{PREMIUM_EMOJIS['fire']} No Abuse | No Spam | No Ads | No NSFW

{PREMIUM_EMOJIS['moon']} **Type** `/help` **For Commands** {PREMIUM_EMOJIS['moon']}

{PREMIUM_EMOJIS['rose']} **Made With ❤️ By Rishu** {PREMIUM_EMOJIS['rose']}
""")

# =======================================================
#                    HELP COMMAND
# =======================================================
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"""
{PREMIUM_EMOJIS['crown']} **Rishu Galaxy Bot Commands** {PREMIUM_EMOJIS['crown']}

**Admin Commands:**
/mute - Mute a user (reply to user)
/unmute - Unmute a user (reply to user)
/kick - Kick user (reply to user)
/ban - Ban user (reply to user)
/unban - Unban user (reply to user)
/promote - Promote to admin (reply to user)
/demote - Demote admin (reply to user)
/lock - Lock group
/unlock - Unlock group

**Owner Commands:**
/off - Turn bot OFF
/on - Turn bot ON
/gcs - Show total GCs
/folder - Show GC links
/unfolder - Remove GC links

{PREMIUM_EMOJIS['rose']} **Made With ❤️ By Rishu** {PREMIUM_EMOJIS['rose']}
""")

# =======================================================
#                    WELCOME NEW MEMBER
# =======================================================
async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if BOT_GLOBALLY_OFF or not update.message or not update.message.new_chat_members:
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
        
        await update.message.reply_text(
            f"""
{PREMIUM_EMOJIS['welcome']}{PREMIUM_EMOJIS['party']}{PREMIUM_EMOJIS['welcome']} **WELCOME TO RISHU GALAXY** {PREMIUM_EMOJIS['welcome']}{PREMIUM_EMOJIS['party']}{PREMIUM_EMOJIS['welcome']}

{PREMIUM_EMOJIS['star']} **Welcome {user_mention}** {PREMIUM_EMOJIS['star']}

{PREMIUM_EMOJIS['gem']} **Name:** {first_name} {PREMIUM_EMOJIS['gem']}
{PREMIUM_EMOJIS['glow']} **Username:** {username} {PREMIUM_EMOJIS['glow']}
{PREMIUM_EMOJIS['sun']} **Day:** {day_str} {PREMIUM_EMOJIS['sun']}
{PREMIUM_EMOJIS['moon']} **Time:** {time_str} {date_str} {PREMIUM_EMOJIS['moon']}
{PREMIUM_EMOJIS['galaxy']} **Group:** {group_name} {PREMIUM_EMOJIS['galaxy']}

{PREMIUM_EMOJIS['heart']} **Made With ❤️ By Rishu** {PREMIUM_EMOJIS['heart']}
""",
            parse_mode='Markdown',
            disable_web_page_preview=True
        )

# =======================================================
#                    OWNER COMMANDS
# =======================================================
@owner_only
async def global_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global BOT_GLOBALLY_OFF
    BOT_GLOBALLY_OFF = True
    await update.message.reply_text(f"{PREMIUM_EMOJIS['moon']} **Bot Turned OFF Globally**")

@owner_only
async def global_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global BOT_GLOBALLY_OFF
    BOT_GLOBALLY_OFF = False
    await update.message.reply_text(f"{PREMIUM_EMOJIS['sun']} **Bot Turned ON Globally**")

# =======================================================
#                    ADMIN COMMANDS
# =======================================================
@admin_only
@check_bot_state
async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text(f"{PREMIUM_EMOJIS['warning']} **Reply to a user!**")
        return
    user = update.message.reply_to_message.from_user
    chat_id = update.effective_chat.id
    try:
        await context.bot.restrict_chat_member(chat_id, user.id, permissions=ChatPermissions(can_send_messages=False))
        await update.message.reply_text(f"{PREMIUM_EMOJIS['muted']} **{user.first_name} Muted!**")
    except Exception as e:
        await update.message.reply_text(f"{PREMIUM_EMOJIS['cross']} **Error: {str(e)}**")

@admin_only
@check_bot_state
async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text(f"{PREMIUM_EMOJIS['warning']} **Reply to a user!**")
        return
    user = update.message.reply_to_message.from_user
    chat_id = update.effective_chat.id
    try:
        await context.bot.restrict_chat_member(
            chat_id, user.id,
            permissions=ChatPermissions(can_send_messages=True, can_send_media_messages=True, 
                                       can_send_other_messages=True, can_send_polls=True, 
                                       can_add_web_page_previews=True)
        )
        await update.message.reply_text(f"{PREMIUM_EMOJIS['unmuted']} **{user.first_name} Unmuted!**")
    except Exception as e:
        await update.message.reply_text(f"{PREMIUM_EMOJIS['cross']} **Error: {str(e)}**")

@admin_only
@check_bot_state
async def kick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text(f"{PREMIUM_EMOJIS['warning']} **Reply to a user!**")
        return
    user = update.message.reply_to_message.from_user
    chat_id = update.effective_chat.id
    try:
        await context.bot.ban_chat_member(chat_id, user.id)
        await context.bot.unban_chat_member(chat_id, user.id)
        await update.message.reply_text(f"{PREMIUM_EMOJIS['kicked']} **{user.first_name} Kicked!**")
    except Exception as e:
        await update.message.reply_text(f"{PREMIUM_EMOJIS['cross']} **Error: {str(e)}**")

@admin_only
@check_bot_state
async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text(f"{PREMIUM_EMOJIS['warning']} **Reply to a user!**")
        return
    user = update.message.reply_to_message.from_user
    chat_id = update.effective_chat.id
    try:
        await context.bot.ban_chat_member(chat_id, user.id)
        await update.message.reply_text(f"{PREMIUM_EMOJIS['banned']} **{user.first_name} Banned!**")
    except Exception as e:
        await update.message.reply_text(f"{PREMIUM_EMOJIS['cross']} **Error: {str(e)}**")

@admin_only
@check_bot_state
async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text(f"{PREMIUM_EMOJIS['warning']} **Reply to a user!**")
        return
    user = update.message.reply_to_message.from_user
    chat_id = update.effective_chat.id
    try:
        await context.bot.unban_chat_member(chat_id, user.id)
        await update.message.reply_text(f"{PREMIUM_EMOJIS['check']} **{user.first_name} Unbanned!**")
    except Exception as e:
        await update.message.reply_text(f"{PREMIUM_EMOJIS['cross']} **Error: {str(e)}**")

@admin_only
@check_bot_state
async def promote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text(f"{PREMIUM_EMOJIS['warning']} **Reply to a user!**")
        return
    user = update.message.reply_to_message.from_user
    chat_id = update.effective_chat.id
    if user.id in OWNER_IDS:
        await update.message.reply_text(f"{PREMIUM_EMOJIS['cross']} **Cannot promote owner!**")
        return
    try:
        await context.bot.promote_chat_member(chat_id, user.id, can_change_info=True, can_invite_users=True,
                                             can_pin_messages=True, can_manage_chat=True, can_delete_messages=True,
                                             can_restrict_members=True, can_promote_members=False)
        await update.message.reply_text(f"{PREMIUM_EMOJIS['promoted']} **{user.first_name} Promoted!**")
    except Exception as e:
        await update.message.reply_text(f"{PREMIUM_EMOJIS['cross']} **Error: {str(e)}**")

@admin_only
@check_bot_state
async def demote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text(f"{PREMIUM_EMOJIS['warning']} **Reply to a user!**")
        return
    user = update.message.reply_to_message.from_user
    chat_id = update.effective_chat.id
    if user.id in OWNER_IDS:
        await update.message.reply_text(f"{PREMIUM_EMOJIS['cross']} **Cannot demote owner!**")
        return
    try:
        await context.bot.promote_chat_member(chat_id, user.id, can_change_info=False, can_invite_users=False,
                                             can_pin_messages=False, can_manage_chat=False, can_delete_messages=False,
                                             can_restrict_members=False, can_promote_members=False)
        await update.message.reply_text(f"{PREMIUM_EMOJIS['demoted']} **{user.first_name} Demoted!**")
    except Exception as e:
        await update.message.reply_text(f"{PREMIUM_EMOJIS['cross']} **Error: {str(e)}**")

@admin_only
@check_bot_state
async def lock_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    try:
        await context.bot.set_chat_permissions(chat_id, ChatPermissions(can_send_messages=False))
        await update.message.reply_text(f"{PREMIUM_EMOJIS['lock']} **Group Locked!**")
    except Exception as e:
        await update.message.reply_text(f"{PREMIUM_EMOJIS['cross']} **Error: {str(e)}**")

@admin_only
@check_bot_state
async def unlock_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    try:
        await context.bot.set_chat_permissions(chat_id, ChatPermissions(can_send_messages=True))
        await update.message.reply_text(f"{PREMIUM_EMOJIS['unlock']} **Group Unlocked!**")
    except Exception as e:
        await update.message.reply_text(f"{PREMIUM_EMOJIS['cross']} **Error: {str(e)}**")

# =======================================================
#                    GC COMMANDS
# =======================================================
@check_bot_state
async def gcs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"{PREMIUM_EMOJIS['galaxy']} **Total GCs ~ {len(GC_LINKS)}**")

@check_bot_state
async def folder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    sent_msgs = []
    for link in GC_LINKS:
        msg = await update.message.reply_text(f"{PREMIUM_EMOJIS['gem']} **GC ~** {link}", disable_web_page_preview=True)
        sent_msgs.append(msg.message_id)
        await asyncio.sleep(0.5)
    folder_messages[chat_id] = sent_msgs

@check_bot_state
async def unfolder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in folder_messages:
        return await update.message.reply_text(f"{PREMIUM_EMOJIS['warning']} **No links to remove!**")
    for msg_id in folder_messages[chat_id]:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
        except:
            pass
    del folder_messages[chat_id]
    await update.message.reply_text(f"{PREMIUM_EMOJIS['check']} **Links Deleted!**")

# =======================================================
#                    LEFT MEMBER HANDLER
# =======================================================
async def left_member_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if BOT_GLOBALLY_OFF or not update.message or not update.message.left_chat_member:
        return

    chat_id = update.effective_chat.id
    group_name = update.effective_chat.title or "Group"
    user = update.message.left_chat_member
    first_name = user.first_name or "User"
    username = f"@{user.username}" if user.username else "N/A"
    msg_date = update.message.date.astimezone(IST)
    time_str = msg_date.strftime("%I:%M %p")
    date_str = msg_date.strftime("%d/%m/%Y")
    day_str = msg_date.strftime("%A")

    leave_msg_text = f"""
{PREMIUM_EMOJIS['galaxy']}{PREMIUM_EMOJIS['sparkle']}{PREMIUM_EMOJIS['galaxy']} **{first_name} Left!** {PREMIUM_EMOJIS['galaxy']}{PREMIUM_EMOJIS['sparkle']}{PREMIUM_EMOJIS['galaxy']}

{PREMIUM_EMOJIS['gem']} Time: {time_str} {date_str}
{PREMIUM_EMOJIS['sun']} Day: {day_str}
{PREMIUM_EMOJIS['glow']} Username: {username}
{PREMIUM_EMOJIS['star']} Group: {group_name}

{PREMIUM_EMOJIS['rocket']} FearOfRishu
"""
    try:
        sent_msg = await update.message.reply_text(leave_msg_text)
        await context.bot.pin_chat_message(chat_id=chat_id, message_id=sent_msg.message_id, disable_notification=True)
    except Exception:
        pass

# =======================================================
#                    ERROR HANDLER
# =======================================================
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f'Error: {context.error}')

# =======================================================
#                    MAIN
# =======================================================
def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("mute", mute))
    app.add_handler(CommandHandler("unmute", unmute))
    app.add_handler(CommandHandler("kick", kick))
    app.add_handler(CommandHandler("ban", ban))
    app.add_handler(CommandHandler("unban", unban))
    app.add_handler(CommandHandler("promote", promote))
    app.add_handler(CommandHandler("demote", demote))
    app.add_handler(CommandHandler("lock", lock_group))
    app.add_handler(CommandHandler("unlock", unlock_group))
    app.add_handler(CommandHandler("gcs", gcs))
    app.add_handler(CommandHandler("folder", folder))
    app.add_handler(CommandHandler("unfolder", unfolder))
    app.add_handler(CommandHandler("off", global_off))
    app.add_handler(CommandHandler("on", global_on))
    
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))
    app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, left_member_handler))
    app.add_error_handler(error_handler)

    print(f"{PREMIUM_EMOJIS['rocket']} Bot is starting...")
    print(f"{PREMIUM_EMOJIS['crown']} Owner IDs: {OWNER_IDS}")
    print(f"{PREMIUM_EMOJIS['check']} Bot token: {TOKEN[:10]}...")
    print(f"{PREMIUM_EMOJIS['sparkle']} Bot is ready!")
    
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
