import re
import uuid
import socket
import platform
import os
import random
import time
import math
import json
import string
import traceback
import psutil
import asyncio
import wget
import motor.motor_asyncio
import pymongo
import aiofiles
import datetime
from pyrogram.errors.exceptions.bad_request_400 import *
from pyrogram.errors import *
from pyrogram import Client, filters
from pyrogram.errors import *
from pyrogram.types import *
from helper.decorators import humanbytes
from config import *
from database.db import Database
from asyncio import *
import heroku3
import requests
from helper.heroku_helper import HerokuHelper
from helper.fsub import forcesub
#--------------------------------------------------Db-------------------------------------------------#


async def send_msg(user_id, message):
    try:
        await message.copy(chat_id=user_id)
        return 200, None
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return send_msg(user_id, message)
    except InputUserDeactivated:
        return 400, f"{user_id} : deactivated\n"
    except UserIsBlocked:
        return 400, f"{user_id} : user is blocked\n"
    except PeerIdInvalid:
        return 400, f"{user_id} : user id invalid\n"
    except Exception as e:
        return 500, f"{user_id} : {traceback.format_exc()}\n"
        
#------------------------------Db End---------------------------------------------------------#       
        

Client = Client(
    "Galkoriya Bot",
    bot_token= BOT_TOKEN,
    api_id= API_ID,
    api_hash= API_HASH,
)

Heroku = heroku3.from_key(HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"


#--------------------------------------configs-------------------------------------------#
start_menu = ReplyKeyboardMarkup(
      [
            ["🤴 OWNER 🤴"]
           
           
        ],
        resize_keyboard=True  # Make the keyboard smaller
    )

next_1 = ReplyKeyboardMarkup(
      [
            ["📊 Statistics"],
            ["BACK 🔙"]
           
        ],
        resize_keyboard=True  # Make the keyboard smaller
      )

back = ReplyKeyboardMarkup(
      [
            ["🤴 OWNER 🤴"]       
           
       ],
        resize_keyboard=True  # Make the keyboard smaller
      )
      
DATABASE_URL=MONGO_URI
db = Database(DATABASE_URL, "Memehub_bot")     
#-------------------------------start---------------------------------------#

@Client.on_message(filters.command("start"))
async def startprivate(client, message):
    if await forcesub(client, message):
       return
    #return
    chat_id = message.from_user.id
    if not await db.is_user_exist(chat_id):
        data = await client.get_me()
        BOT_USERNAME = data.username
        await db.add_user(chat_id)
        if LOG_CHANNEL:
            await client.send_message(
                LOG_CHANNEL,
                f"#NEWUSER: \n\n**User:** [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n**ID:**{message.from_user.id}\n Started @{BOT_USERNAME} !!",
            )
            await client.send_message(
                PRIVATE_LOG,
                f"#NEWUSER: \n\n**User:** [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n**ID:**{message.from_user.id}\n Started @{BOT_USERNAME} !!"
            )    
        else:
            logging.info(f"#NewUser :- Name : {message.from_user.first_name} ID : {message.from_user.id}")
    file_id = "CAADBQADSwQAAnxrOFaYSIaXhBE_YAI"
    await client.send_sticker(message.chat.id, file_id, reply_markup=start_menu)
    text = f"Hi {message.from_user.mention}, Welcome to  Jollyathal Telegram 🇱🇰 Official Bot"
    reply_markup = START_BUTTON  
    await message.reply_text(
        text=text,
        reply_markup=reply_markup,
        disable_web_page_preview=True,
        quote=True
    )
    
@Client.on_message(filters.incoming & filters.chat(-1001645439750))
async def bchanl(bot, update, broadcast_ids={}): 
    all_users = await db.get_all_users()
    broadcast_msg= update
    while True:
        broadcast_id = ''.join([random.choice(string.ascii_letters) for i in range(3)])
        if not broadcast_ids.get(broadcast_id):
            break

    out = await bot.send_message(-1001689365631,f"Ads Broadcast Started! You will be notified with log file when all the users are notified.")
    start_time = time.time()
    total_users = await db.total_users_count()
    done = 0
    failed = 0
    success = 0
    broadcast_ids[broadcast_id] = dict(total = total_users, current = done, failed = failed, success = success)
        
    async with aiofiles.open('broadcastlog.txt', 'w') as broadcast_log_file:
        async for user in all_users:
            sts, msg = await send_msg(user_id = int(user['id']), message = broadcast_msg)
            if msg is not None:
                await broadcast_log_file.write(msg)
            if sts == 200:
                success += 1
            else:
                failed += 1
            if sts == 400:
                await db.delete_user(user['id'])
            done += 1
            if broadcast_ids.get(broadcast_id) is None:
                break
            else:
                broadcast_ids[broadcast_id].update(dict(current = done, failed = failed, success = success))
        
    if broadcast_ids.get(broadcast_id):
        broadcast_ids.pop(broadcast_id)
    
    completed_in = datetime.timedelta(seconds=int(time.time()-start_time))
    await asyncio.sleep(3)
    await out.delete()
    
    if failed == 0:
        await bot.send_message(-1001689365631, f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.")
    else:
        await bot.send_document(-1001689365631, 'broadcastlog.txt', caption=f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.")
    os.remove('broadcastlog.txt') 
    
        
#-------------------------------------------menu Regex-----------------------------------------#         
  
@Client.on_message(filters.regex(pattern="🤴 OWNER 🤴"))   
async def startprivate(bot, message):
     await bot.send_sticker(message.chat.id, random.choice(OWNER_STICKER),reply_markup=OWNER_BTN)

@Client.on_message(filters.regex(pattern="📊 Statistics"))   
async def startprivate(bot, message):
    splatform = platform.system()
    platform_release = platform.release()
    platform_version = platform.version()
    architecture = platform.machine()
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(socket.gethostname())
    mac_address = ":".join(re.findall("..", "%012x" % uuid.getnode()))
    processor = platform.processor()
    ram = humanbytes(round(psutil.virtual_memory().total))
    cpu_freq = psutil.cpu_freq().current
    if cpu_freq >= 1000:
        cpu_freq = f"{round(cpu_freq / 1000, 2)}GHz"
    else:
        cpu_freq = f"{round(cpu_freq, 2)}MHz"
    du = psutil.disk_usage(bot.workdir)
    psutil.disk_io_counters()
    disk = f"{humanbytes(du.used)} / {humanbytes(du.total)} " f"({du.percent}%)"
    cpu_len = len(psutil.Process().cpu_affinity())
    countb = await db.total_users_count()
    countb = await db.total_users_count()
    count = await bot.get_chat_members_count(-1001210985373)
    counta = await bot.get_chat_members_count(-1001759991131)
    text=f"""**Bot Advanced Statistics 📊**
** 👥Members Counts in Our channel:**

◉──────────────────────────────────◉
 **Jollyathal Telegram 🇱🇰  Users** : `{count}`
 **⚜️Jollyathal Family⚜️ (Admins)**   : `{counta}`
 **Jollyathal ᴏᴍғғɪᴄɪᴀʟ ʙᴏᴍᴛ 『🇱🇰』 Users** : `{countb}`
◉──────────────────────────────────◉
🖥 **System Information**

**PlatForm :** `{splatform}`
**PlatForm - Release :** `{platform_release}`
**PlatFork - Version :** `{platform_version}`
**Architecture :** `{architecture}`
**Hostname :** `{hostname}`
**IP :** `{ip_address}`
**Mac :** `{mac_address}`
**Processor :** `{processor}`
**Ram : ** `{ram}`
**CPU :** `{cpu_len}`
**CPU FREQ :** `{cpu_freq}`
**DISK :** `{disk}`
◉──────────────────────────────────◉
 """
 
    await bot.send_sticker(message.chat.id, random.choice(STAT_STICKER))
    await bot.send_message(message.chat.id, text=text)

@Client.on_message(filters.regex(pattern="💻 Bot Devs 💻"))   
async def startprivate(bot, message):
     await bot.send_sticker(message.chat.id, random.choice(DEV_STICKER),reply_markup=DEV_BTN)

@Client.on_message(filters.regex(pattern="👮‍♂️  Admins 👮‍♂️"))   
async def startprivate(bot, message):
     await bot.send_sticker(message.chat.id, random.choice(ADMIN_STICKER),reply_markup=ADMIN_BTN)
    
@Client.on_message(filters.regex(pattern="NEXT 🔜"))   
async def startprivate(bot, message):
     await bot.send_message(message.chat.id, text='NEXT 🔜',reply_markup=next_1)
        
@Client.on_message(filters.regex(pattern="BACK 🔙"))   
async def startprivate(bot, message):
     await bot.send_message(message.chat.id, text='BACK 🔙',reply_markup=start_menu)

#-----------------------------------------update--------------------------------------------------#
@Client.on_message(filters.command("carupd"))
async def on_off_antiarab(bot, message):
    if message.from_user.id not in AUTH_USERS:
        await message.delete()
        return
    UPDT_NT=" ".join(message.command[2:])
    photo=message.command[1]
    caption=f"""
 #UPDATE 

**Update Available**

{UPDT_NT}

By : {message.from_user.mention}
    """
    await bot.send_photo(message.chat.id,photo=photo, caption=caption, reply_markup=InlineKeyboardMarkup([[              
                 InlineKeyboardButton('♻️ Updatate ♻️', callback_data="upd")
                 ]]
                  )
    ) 

    
@Client.on_message(filters.command("upd"))
async def on_off_antiarab(bot, message):
    if message.from_user.id not in AUTH_USERS:
        await message.delete()
        return
    f= message.text
    s=f.replace('/upd ' ,'')
    UPDATE_N=s.replace('%20', ' ')
    text = f"""
#UPDATE

╭━╮╭━╮
┃┃╰╯┃
┃╭╮╭╮ |
┃┃┃┃┃┃
┃┃┃┃┃┃
╰╯╰╯╰

**Update Available**

◇─────Update Note─────◇
        
{UPDATE_N}

By : {message.from_user.mention}
    """
    await message.reply_text(text=text, reply_markup=InlineKeyboardMarkup([[              
                 InlineKeyboardButton('♻️ Updatate ♻️', callback_data="upd")
                 ]]
                  )
    )
#----------------------------------------------admin Cmds---------------------------------------------#

@Client.on_message(filters.private & filters.command("ban"))
async def ban(c, m):
    if m.from_user.id not in AUTH_USERS:
        await m.delete()
        return
    if len(m.command) == 1:
        await m.reply_text(
            f"Use this command to ban 🛑 any user from the bot 🤖.\n\nUsage:\n\n`/ban_user user_id ban_duration ban_reason`\n\nEg: `/ban_user 1234567 28 You misused me.`\n This will ban user with id `1234567` for `28` days for the reason `You misused me`.",
            quote=True,
        )
        return

    try:
        user_id = int(m.command[1])
        ban_duration = int(m.command[2])
        ban_reason = " ".join(m.command[3:])
        ban_log_text = f"Banning user {user_id} for {ban_duration} days for the reason {ban_reason}."

        try:
            await c.send_message(
                user_id,
                f"You are Banned 🚫 to use this bot for **{ban_duration}** day(s) for the reason __{ban_reason}__ \n\n**Message from the admin 🤠**",
            )
            
            ban_log_text += "\n\nUser notified successfully!"
            await c.send_message(PRIVATE_LOG,text=f"""#BAN_LOG

• **Of:** {m.from_user.mention} [`{m.from_user.id}`]
• **To:** [User](tg://user?id={user_id}) [`{user_id}`]
• **Reason:** {ban_reason}
• **Duration:** {ban_duration} day(s)
""")
     
        except BaseException:
            traceback.print_exc()
            ban_log_text += (
                f"\n\n ⚠️ User notification failed! ⚠️ \n\n`{traceback.format_exc()}`"
            )
        await db.ban_user(user_id, ban_duration, ban_reason)
        print(ban_log_text)
        await m.reply_text(ban_log_text, quote=True)
    except BaseException:
        traceback.print_exc()
        await m.reply_text(
            f"Error occoured ⚠️! Traceback given below\n\n`{traceback.format_exc()}`",
            quote=True
        )
 
@Client.on_message(filters.private & filters.command("unban"))
async def unban(c, m):
    if m.from_user.id not in AUTH_USERS:
        await m.delete()
        return
    if len(m.command) == 1:
        await m.reply_text(
            f"Use this command to unban 😃 any user.\n\nUsage:\n\n`/unban_user user_id`\n\nEg: `/unban_user 1234567`\n This will unban user with id `1234567`.",
            quote=True,
        )
        return

    try:
        user_id = int(m.command[1])
        unban_log_text = f"Unbanning user 🤪 {user_id}"
        await c.send_message(PRIVATE_LOG,text=f"""#UNBAN_LOG

• **Of:** {m.from_user.mention} [`{m.from_user.id}`]
• **To:** [User](tg://user?id={user_id}) [`{user_id}`]
""")

        try:
            await c.send_message(user_id, f"Your ban was lifted!")
            unban_log_text += "\n\n✅ User notified successfully! ✅"
        except BaseException:
            traceback.print_exc()
            unban_log_text += (
                f"\n\n⚠️ User notification failed! ⚠️\n\n`{traceback.format_exc()}`"
            )
        await db.remove_ban(user_id)
        print(unban_log_text)
        await m.reply_text(unban_log_text, quote=True)
    except BaseException:
        traceback.print_exc()
        await m.reply_text(
            f"⚠️ Error occoured ⚠️! Traceback given below\n\n`{traceback.format_exc()}`",
            quote=True,
        )


@Client.on_message(filters.private & filters.command("listbanned"))
async def _banned_usrs(c, m):
    if m.from_user.id not in AUTH_USERS:
        await m.delete()
        return
    all_banned_users = await db.get_all_banned_users()
    banned_usr_count = 0
    text = ""
    async for banned_user in all_banned_users:
        user_id = banned_user["id"]
        ban_duration = banned_user["ban_status"]["ban_duration"]
        banned_on = banned_user["ban_status"]["banned_on"]
        ban_reason = banned_user["ban_status"]["ban_reason"]
        banned_usr_count += 1
        text += f"> **User_id**: `{user_id}`, **Ban Duration**: `{ban_duration}`, **Banned on**: `{banned_on}`, **Reason**: `{ban_reason}`\n\n"
    reply_text = f"Total banned user(s) 🤭: `{banned_usr_count}`\n\n{text}"
    if len(reply_text) > 4096:
        with open("banned-users.txt", "w") as f:
            f.write(reply_text)
        await m.reply_document("banned-users.txt", True)
        os.remove("banned-users.txt")
        return
    await m.reply_text(reply_text, True)
    
#----------------------------------------------heroku Cmds---------------------------------------------#
@Client.on_message(filters.command("logs"))
async def giblog(bot, message):
    if message.from_user.id not in AUTH_USERS:
        await message.delete()
        return
    process = await message.reply_text( "`Trying To Fetch Logs....`")
    herokuHelper = HerokuHelper(HEROKU_APP_NAME, HEROKU_API_KEY)
    logz = herokuHelper.getLog()
    with open("logs.txt", "w") as log:
        log.write(logz)
    await process.delete()
    await bot.send_document(
        message.chat.id, "logs.txt", caption=f"**Logs Of {HEROKU_APP_NAME}**"
    )
    os.remove("logs.txt")


@Client.on_message(filters.command("restart"))
async def restart_me(bot, message):
    if message.from_user.id not in AUTH_USERS:
        await message.delete()
        return
    herokuHelper = HerokuHelper(HEROKU_APP_NAME, HEROKU_API_KEY)
    await message.reply_text("`App is Restarting. This is May Take Upto 3Min.`", quote=True)
    herokuHelper.restart()


@Client.on_message(filters.command("usage"))
async def dyno_usage(bot, message):
    if message.from_user.id not in AUTH_USERS:
        await message.delete()
        return
    process = await message.reply_text( "`Trying To Fetch Dyno Usage....`")
    useragent = (
        "Mozilla/5.0 (Linux; Android 10; SM-G975F) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/80.0.3987.149 Mobile Safari/537.36"
    )
    user_id = Heroku.account().id
    headers = {
        "User-Agent": useragent,
        "Authorization": f"Bearer {HEROKU_API_KEY}",
        "Accept": "application/vnd.heroku+json; version=3.account-quotas",
    }
    path = "/accounts/" + user_id + "/actions/get-quota"
    r = requests.get(heroku_api + path, headers=headers)
    if r.status_code != 200:
        return await message.reply_text(
             "`Error: something bad happened`\n\n" f">.`{r.reason}`\n"
        )
    result = r.json()
    quota = result["account_quota"]
    quota_used = result["quota_used"]

    """ - Used - """
    remaining_quota = quota - quota_used
    percentage = math.floor(remaining_quota / quota * 100)
    minutes_remaining = remaining_quota / 60
    hours = math.floor(minutes_remaining / 60)
    minutes = math.floor(minutes_remaining % 60)

    """ - Current - """
    App = result["apps"]
    try:
        App[0]["quota_used"]
    except IndexError:
        AppQuotaUsed = 0
        AppPercentage = 0
    else:
        AppQuotaUsed = App[0]["quota_used"] / 60
        AppPercentage = math.floor(App[0]["quota_used"] * 100 / quota)
    AppHours = math.floor(AppQuotaUsed / 60)
    AppMinutes = math.floor(AppQuotaUsed % 60)

    await asyncio.sleep(1.5)

    return await process.edit(
        "**Dyno Usage Data**:\n\n"
        f"✗ **APP NAME =>** `{HEROKU_APP_NAME}` \n"
        f"✗ **Usage in Hours And Minutes =>** `{AppHours}h`  `{AppMinutes}m`"
        f"✗ **Usage Percentage =>** [`{AppPercentage} %`]\n"
        "\n\n"
        "✗ **Dyno Remaining This Months 📆:**\n"
        f"✗ `{hours}`**h**  `{minutes}`**m** \n"
        f"✗ **Percentage :-** [`{percentage}`**%**]",
    )
#----------------------------------------------main Cmds---------------------------------------------#

@Client.on_message(filters.command("send"))
async def status(bot, message):
    if message.from_user.id not in AUTH_USERS:
        await message.delete()
        return
    mesg=message.reply_to_message
    f= message.text
    s=f.replace('/send ' ,'')
    fid=s.replace('%20', ' ')
    await send_msg(user_id=fid, message=mesg)
    await message.delete()
    await bot.send_message(message.chat.id, text=f"Ur Msg Sent To [User](tg://user?id={fid})", reply_markup=CLOSE_BUTTON)
    await bot.send_message(PRIVATE_LOG,text=f"""#SEND_LOG

• **Send By:** {message.from_user.mention} [`{message.from_user.id}`]
• **Send To:** [User](tg://user?id={fid}) [`{fid}`]
• **Message:-**
""")
    await send_msg(PRIVATE_LOG, message=mesg)
                          
@Client.on_message(filters.private &filters.command("admincast"))
async def status(bot, message):
    if message.from_user.id not in AUTH_USERS:
        await message.delete()
        return
    msg=message.reply_to_message
    await send_msg(user_id=1884885842, message=msg)
    await send_msg(user_id=5115331277, message=msg)
    await send_msg(user_id=5025877489, message=msg)
    await send_msg(user_id=1202064253, message=msg)
    await send_msg(user_id=1120271521, message=msg)
    await send_msg(user_id=1235760387, message=msg)
    await send_msg(user_id=LOG_CHANNEL, message=msg)
    await bot.send_message(PRIVATE_LOG,text=f"""GADMINCAST_LOG

• **Of:** {message.from_user.mention} [`{message.from_user.id}`]
""")
        
@Client.on_message(filters.command(["help", "help@Jollyathall2bot"]))
async def help(bot, message):
    if await forcesub(bot, message):
       return
    await bot.send_sticker(message.chat.id, random.choice(HELP_STICKER), reply_markup=start_menu)
    await message.reply_text(
        text=HELP_STRING,
        reply_markup=CLOSE_BUTTON,
        disable_web_page_preview=True
         )

@Client.on_message(filters.private & filters.command("status"), group=5)
async def status(bot, update):
    if update.from_user.id not in AUTH_USERS:
        await message.delete()
        return
    if not await db.is_user_exist(update.from_user.id):
         await db.add_user(update.from_user.id)
         
    await bot.send_sticker(update.chat.id, random.choice(STAT_STICKER))
    total_users = await db.total_users_count()
    text = "**Bot Advanced Statistics 📊**\n"
    text += f"\n**Total Users:** `{total_users}`"

    await update.reply_text(
        text=text,
        quote=True,
        disable_web_page_preview=True
    )

@Client.on_message(
    filters.private &
    filters.command("broadcast") &
    filters.reply
)
async def broadcast(bot, update, broadcast_ids={}):
    if update.from_user.id not in AUTH_USERS:
        await message.delete()
        return
    
    all_users = await db.get_all_users()
    broadcast_msg= update.reply_to_message
    while True:
        broadcast_id = ''.join([random.choice(string.ascii_letters) for i in range(3)])
        if not broadcast_ids.get(broadcast_id):
            break

    out = await update.reply_text(text=f"Broadcast Started! You will be notified with log file when all the users are notified.")
    start_time = time.time()
    total_users = await db.total_users_count()
    done = 0
    failed = 0
    success = 0
    broadcast_ids[broadcast_id] = dict(total = total_users, current = done, failed = failed, success = success)
        
    async with aiofiles.open('broadcast.txt', 'w') as broadcast_log_file:
        async for user in all_users:
            sts, msg = await send_msg(user_id = int(user['id']), message = broadcast_msg)
            if msg is not None:
                await broadcast_log_file.write(msg)
            if sts == 200:
                success += 1
            else:
                failed += 1
            if sts == 400:
                await db.delete_user(user['id'])
            done += 1
            if broadcast_ids.get(broadcast_id) is None:
                break
            else:
                broadcast_ids[broadcast_id].update(dict(current = done, failed = failed, success = success))
        
    if broadcast_ids.get(broadcast_id):
        broadcast_ids.pop(broadcast_id)
    
    completed_in = datetime.timedelta(seconds=int(time.time()-start_time))
    await asyncio.sleep(3)
    await out.delete()

    if failed == 0:
        await update.reply_text(text=f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.", quote=True)
        await bot.send_message(PRIVATE_LOG,text=f"""#BROADCAST_LOG

• **Of:** {update.from_user.mention} [`{update.from_user.id}`]
""")
    else:
        await update.reply_document(document='broadcast.txt', caption=f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.")
        await bot.send_message(PRIVATE_LOG,text=f"""#BROADCAST_LOG

• **Of:** {update.from_user.mention} [`{update.from_user.id}`]
""")
    os.remove('broadcast.txt') 

                       
print("cmds.py Working....")  

#------------------------------------------------Pm----------------------------------------------------#

@Client.on_message(filters.chat(LOG_CHANNEL) & filters.command("info"))
async def replay_media(bot, message):
    file = message.reply_to_message
    reference_id = file.text.split()[2]
    info = await bot.get_users(user_ids=reference_id)
    await bot.send_message(message.from_user.id, text=f"""
    **User Info**
    
    **••User id:** [`{info.id}`]
    **••First Name:** {info.first_name}
    **••UserName:** @{info.username}
    
    """)

@Client.on_message(filters.private & filters.text)
async def pm_text(bot, message):
    if message.from_user.id == OWNER_ID:
        await reply_text(bot, message)
        return
    if await forcesub(bot, message):
       return
    info = await bot.get_users(user_ids=message.from_user.id)
    reference_id = int(message.chat.id)
    await bot.send_message(
        chat_id=OWNER_ID,
        text=PM_TXT_ATT.format(reference_id, info.first_name, message.text)
    )
    await bot.send_message(
        chat_id=LOG_CHANNEL,
        text=PM_TXT_ATT.format(reference_id, info.first_name, message.text)
    )
    

@Client.on_message(filters.private & filters.sticker)
async def pm_sticker(bot, message):
    if message.from_user.id == OWNER_ID:
        await replay_media(bot, message)
        return
    if await forcesub(bot, message):
       return
    info = await bot.get_users(user_ids=message.from_user.id)
    reference_id = int(message.chat.id)
    await bot.copy_message(
        chat_id=OWNER_ID,
        from_chat_id=message.chat.id,
        message_id=message.id
    )
    await bot.send_message(OWNER_ID, text=PM_TXT_ATTS.format(reference_id, info.first_name))
    await bot.copy_message(
        chat_id=LOG_CHANNEL,
        from_chat_id=message.chat.id,
        message_id=message.id
    )
    await bot.send_message(LOG_CHANNEL, text=PM_TXT_ATTS.format(reference_id, info.first_name))
    
@Client.on_message(filters.private & filters.media)
async def pm_media(bot, message):
    if message.from_user.id == OWNER_ID:
        await replay_media(bot, message)
        return
    if await forcesub(bot, message):
       return
    await message.reply_text(text=f"Ur Photo Sent To @jollyathal Admins", reply_markup=CLOSE_BUTTON)
    info = await bot.get_users(user_ids=message.from_user.id)
    reference_id = int(message.chat.id)
    msg=message.caption
    await bot.copy_message(
        chat_id=OWNER_ID,       
        from_chat_id=message.chat.id,
        message_id=message.id,
        caption=PM_MED_ATT.format(reference_id, message.from_user.mention, msg)
    )
    reference_id = int(message.chat.id)
    msg=message.caption
    await bot.copy_message(
        chat_id=LOG_CHANNEL,
        from_chat_id=message.chat.id,
        message_id=message.id,
        caption=PM_MED_ATT.format(reference_id, message.from_user.mention, msg),
        reply_markup=InlineKeyboardMarkup([[
                 InlineKeyboardButton("✅ᴀᴄᴄᴇᴘᴛ", callback_data="acce"),
                 InlineKeyboardButton("❌ʀᴇᴊᴇᴄᴛ", callback_data="cloc")
                 ]]
                 )
    )
    


@Client.on_message(filters.text)
async def reply_text(bot, message):
    reference_id = True
    if message.reply_to_message is not None:
        file = message.reply_to_message
        try:
            reference_id = file.text.split()[2]
        except Exception:
            pass
        try:
            reference_id = file.caption.split()[2]
        except Exception:
            pass
        await bot.send_message(
            text=f"**Msg From**:{message.from_user.mention}\n\n{message.text}",
            chat_id=int(reference_id)
        )


@Client.on_message(filters.media)
async def replay_media(bot, message):
    reference_id = True
    if message.reply_to_message is not None:
        file = message.reply_to_message
        try:
            reference_id = file.text.split()[2]
        except Exception:
            pass
        try:
            reference_id = file.caption.split()[2]
        except Exception:
            pass
        await bot.copy_message(
            chat_id=int(reference_id),
            from_chat_id=message.chat.id,
            message_id=message.id
        )
@Client.on_message(filters.private & filters.text)
async def pm_text(bot, message):
    if message.from_user.id == OWNER_ID:
        await reply_text(bot, message)
        return
    if await forcesub( bot,update):
       return
    info = await bot.get_users(user_ids=message.from_user.id)
    reference_id = int(message.chat.id)
    await bot.send_message(
        chat_id=OWNER_ID,
        text=PM_TXT_ATT.format(reference_id, info.first_name, message.text)
    )


@Client.on_message(filters.private & filters.media)
async def pm_media(bot, message):
    if message.from_user.id == OWNER_ID:
        await replay_media(bot, message)
        return
    if await forcesub( bot,update):
       return
    info = await bot.get_users(user_ids=message.from_user.id)
    reference_id = int(message.chat.id)
    await bot.copy_message(
        chat_id=OWNER_ID,
        from_chat_id=message.chat.id,
        message_id=message.message_id,
        caption=PM_MED_ATT.format(reference_id, info.first_name)
    )


@Client.on_message(filters.text)
async def reply_text(bot, message):
    reference_id = True
    if message.reply_to_message is not None:
        file = message.reply_to_message
        try:
            reference_id = file.text.split()[2]
        except Exception:
            pass
        try:
            reference_id = file.caption.split()[2]
        except Exception:
            pass
        await bot.send_message(
            text=message.text,
            chat_id=int(reference_id)
        )


@Client.on_message(filters.media)
async def replay_media(bot, message):
    reference_id = True
    if message.reply_to_message is not None:
        file = message.reply_to_message
        try:
            reference_id = file.text.split()[2]
        except Exception:
            pass
        try:
            reference_id = file.caption.split()[2]
        except Exception:
            pass
        await bot.copy_message(
            chat_id=int(reference_id),
            from_chat_id=message.chat.id,
            message_id=message.id
        )
print("Pm Working....")


#------------------------------------------------Callback-------------------------------------------#
@Client.on_callback_query()  
async def tgm(bot, update):  
    if update.data == "add": 
        await update.answer(
             text="♻️Adding Soon.....",
        )
    elif update.data == "bak":
         await update.message.edit_text(
             text=HELP_STRING,
             reply_markup=CLOSE_BUTTON,
             disable_web_page_preview=True
         )
         await update.answer(
             text="👻 ʙᴀᴍᴄᴋ 👻",
         )
    elif update.data == "bak":
         await update.message.delete()
         await bot.delete_message(update.chat.id, update.message.id)
    elif update.data == "hlp":
         await update.message.edit_text(
             text=HELP_STRING,
             reply_markup=CLOSE_BUTTON,
             disable_web_page_preview=True
         )
         await update.answer(
             text="👻 ʜᴇᴍʟᴘ 👻",
         )
    elif update.data == "cloce":
        await update.message.delete()
    elif update.data == "ref": 
        await update.answer("♻️Reloading.....♻️",) 
        await update.message.delete()
        if await forcesub(bot, update):
            return
        file_id = "CAADBQADowwAAretqFR36va45QlD0gI"
        await bot.send_sticker(update.from_user.id, file_id, reply_markup=start_menu)
        TEXT = f"Hi {update.from_user.mention}, Welcome to  Jollyathal Telegram 🇱🇰 Official Bot"
        RMB = START_BUTTON  
        await bot.send_message(update.from_user.id, TEXT, reply_markup=RMB, disable_web_page_preview=True)
        
    elif update.data == "cloc":
        if update.from_user.id not in AUTH_USERS:
            await update.answer(
                 text="❌ ʏᴏᴜ'ʀᴇ ɴᴏᴛ ʙᴏᴛ ᴀᴅᴍɪɴ ❌",
            ) 
            return
        await update.message.delete()
        rid=update.message.caption.split()[2]
        await bot.send_message(rid, text=f"☠️ **Ur Message Rejected By {update.from_user.mention}** ☠️")
        c_id = str(LOG_CHANNEL)[4:]
        await bot.send_message(PRIVATE_LOG,text=f"""#REJECT_LOG

• **Of:** {update.from_user.mention} [`{update.from_user.id}`]
• **Post:** https://t.me/c/{c_id}/{update.message.id}
""")
    elif update.data == "upd":
        await update.message.edit_text("Updating....")
        await update.answer(
             text="♻️ Updatating Please Wait ♻️",
        )
        await update.message.edit("**♻️ Updatating ♻️ -**") 
        await update.message.edit("**♻️ Updatating ♻️ \**") 
        await update.message.edit("**♻️ Updatating ♻️ |**")
        await update.message.edit("**♻️ Updatating ♻️ /**")
        await update.message.edit("**♻️ Updatating ♻️ -**") 
        await update.message.edit("**♻️ Updatating ♻️ \**") 
        await update.message.edit("**♻️ Updatating ♻️ |**")
        await update.message.edit("**♻️ Updatating ♻️ /**")
        await update.message.edit("**♻️ Updatating ♻️ -**") 
        await update.message.edit("**♻️ Updatating ♻️ \**") 
        await update.message.edit("**♻️ Updatating ♻️ |**")
        await update.message.edit("**♻️ Updatating ♻️ /**")
        await update.message.edit("**♻️ Updatating ♻️ -**") 
        await update.message.edit("**♻️ Updatating ♻️ \**") 
        await update.message.edit("**♻️ Updatating ♻️ |**")
        await update.message.edit("**♻️ Updatating ♻️ /**")
        await update.message.edit("**♻️ Updatating ♻️ -**") 
        await update.message.edit("**♻️ Updatating ♻️ \**") 
        await update.message.edit("**♻️ Updatating ♻️ |**")
        await update.message.edit("**♻️ Updatating ♻️ /**")
        await update.message.edit("**♻️ Updatating ♻️ -**") 
        await update.message.edit("**♻️ Updatating ♻️ \**") 
        await update.answer(
             text="♻️ Updated ♻️",
        )
        await update.message.edit(text="**♻️----Updated----♻️**", reply_markup=CLOSE_BUTTON)
    elif update.data == "acce":
        if update.from_user.id not in AUTH_USERS:
            await update.answer(
                 text="❌ ʏᴏᴜ'ʀᴇ ɴᴏᴛ ʙᴏᴛ ᴀᴅᴍɪɴ ❌",
            ) 
            return
        info = await bot.get_users(user_ids=update.message.from_user.id)
        reference_id = int(update.message.chat.id)
        process = await bot.copy_message(
        chat_id=MAIN_CHANNEL,
        from_chat_id=LOG_CHANNEL,
        message_id=update.message.id,
        caption=f"{update.message.caption}\n\n<b>Accept By:</b>{update.from_user.mention}"
    )
        await update.message.delete()
        rid=update.message.caption.split()[2]
        file_id="CAADBAADBwkAAmAw-FKQ4jfoM0moPwI"
        await bot.send_sticker(rid, file_id)
        msg_id = process.id
        rid=update.message.caption.split()[2]
        await bot.send_message(rid, text=f"🎉 [ᴛʜɪs](https://t.me/{force_subchannel}/{msg_id}) ᴘᴏsᴛ ᴀᴄᴄᴇᴘᴛᴇᴅ 🎉", disable_web_page_preview=True)
        
        await update.answer(
             text="✅ᴍᴇssᴀɢᴇ ᴀᴄᴄᴇᴘᴛᴇᴅ",
        )
        await bot.send_message(PRIVATE_LOG,text=f"""#APPROVE_LOG

• **Of:** {update.from_user.mention} [`{update.from_user.id}`]
• **Post:** https://t.me/{force_subchannel}/{msg_id}
""")
#--------------------------------------------------Inline------------------------------------------------#

@Client.on_inline_query()
async def answer(client, inline_query):
   if inline_query.query=='share':
        await inline_query.answer(
            results=[
                InlineQueryResultVideo(
                    title="Share Karapam",
                    video_url="https://telegra.ph/file/d58df8b002dfba939c9a8.mp4",
                    thumb_url="https://telegra.ph/file/7c8846dcae3767b15e3c0.jpg",
                    caption=f"""
𝙷𝚒. 𝙱𝚘𝚢𝚜 𝚊𝚗𝚍 𝚐𝚒𝚛𝚕𝚜 𝚠𝚎 𝚊𝚛𝚎 𝚝𝚑𝚎 𝚖𝚎𝚖𝚎𝚑𝚞𝚋 𝚒𝚏 𝚢𝚘𝚞 𝚑𝚊𝚟𝚎 𝚖𝚎𝚖𝚎𝚜 𝚜𝚎𝚗𝚍 𝚢𝚘𝚞𝚛 𝚖𝚎𝚖𝚎𝚜 𝚝𝚘 𝚘𝚞𝚛 𝚋𝚘𝚝 𝚊𝚗𝚍 𝚑𝚎𝚕𝚙 𝚞𝚜.
𝙼𝚎𝚖𝚎𝚑𝚞𝚋 එකේ ඇඩ්මින් නැ කියල දුකෙම්ද ඉන්නේ 𝚖𝚎𝚖𝚎𝚜 ගොඩගැහිලා ඒවාට කරගන්න දෙයක් නේද? මෙන්න විසදුම ඔයාගේ 𝚖𝚎𝚖𝚎𝚜/𝚏𝚞𝚗𝚗𝚢 𝚟𝚒𝚍𝚎𝚘𝚜 ඔක්කොම එවන්න අපිට අපි ඒවා දානවා අපේ 𝚌𝚑𝚊𝚗𝚗𝚎𝚕 එකේ ඒ අතරින් හැමදාම 𝚖𝚎𝚖𝚜 දාන අයට අපේ 𝚌𝚑𝚊𝚗𝚗𝚎𝚕 එකේ ඇඩ්මින් වෙන්නත් පුළුවන් අදම එක්වන්න අප සමග 🤞✌️🤟🤘👊
𝙱𝚘𝚝 = @MemehubTgSl_Bot

Post By {inline_query.from_user.mention}
""",
                    reply_markup=InlineKeyboardMarkup([[              
                 InlineKeyboardButton('🍁 Owner 🍁', user_id="@chari_x")
                 ],
                 [
                 InlineKeyboardButton('🐞 Report Bugs 🐞', user_id="1195158318")
                 ],
                 [
                 InlineKeyboardButton('Galkoriya ᴏᴍғғɪᴄɪᴀʟ ʙᴏᴍᴛ 『🇱🇰』', user_id="@jollyathall2bot")
                 ],
                 [
                 InlineKeyboardButton("➕ sʜᴀʀᴇ ʙᴏᴛ ➕", switch_inline_query="share"),
                 InlineKeyboardButton("➕ sʜᴀʀᴇ ᴄʜɴʟ ➕", switch_inline_query="cshare")
                 ]])
                    
                        
                     
            ),
            ],
            cache_time=1
        ) 
   if inline_query.query=='cshare':
        await inline_query.answer(
            results=[
                InlineQueryResultPhoto(
                    title="Share Karapam",
                    photo_url="https://telegra.ph/file/f222ad812944e67c57e58.jpg",
                    caption=f"""
අපි තමා Telegram වල හොඳටම කරලා තියෙන්නේ...😎❤️


සමාවෙන්න මට වැරදුනා...🥺😂



**Post by**: {inline_query.from_user.mention}
""",
                    reply_markup=InlineKeyboardMarkup([[              
                 InlineKeyboardButton("Galkoriya Telegram 🇱🇰', url=t.me/jollyathall")
                 ],
                 [
                 InlineKeyboardButton('Owner 👑', user_id="@chari_x")
                 ],
                 [
                 InlineKeyboardButton('Official Bot🤖', user_id="@jollyathall2bot")
                 ]])
                 

         
            ),
            ],
            cache_time=1
        )     
print("""
░███████╗░██╗░░██╗░█████╗░  
██╔██╔══██╗██║░░██║██╔══██╗  
██████████╔╝███████║███████║  
██░██╔═══╝░██╔══██║██╔══██║  
██╗██║░░░░░██║░░██║██║░░██║  
╚═╝░░░░░╚═╝░░╚═╝╚═╝░░╚═╝  

▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
➖➖➖➖➖➖➖➖➖➖
@jollyathall2bot has been deployed!
➖➖➖➖➖➖➖➖➖➖
Support: @jollyathall
➖➖➖➖➖➖➖➖➖➖
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
""")



print(" Deployed Successfully !")        
Client.run()

