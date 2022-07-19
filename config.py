import os
import random

from pyrogram.errors.exceptions.bad_request_400 import *
from pyrogram.errors import *
from pyrogram import Client, filters
from pyrogram.errors import *
from pyrogram.types import *

#Vars
HEROKU_API_KEY = os.getenv("HEROKU_API_KEY", "")
HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME", "")
BOT_TOKEN = os.getenv("BOT_TOKEN")  # from @botfather
API_ID = int(os.getenv("API_ID"))  # from https://my.telegram.org/apps
API_HASH = os.getenv("API_HASH")  # from https://my.telegram.org/apps
AUTH_USERS = set(int(x) for x in os.environ.get("AUTH_USERS", "1195158318 ").split())
MONGO_URI = os.getenv("MONGO_URI")
MAIN_CHANNEL = int(os.environ.get("MAIN_CHANNEL", "-1001618208549"))
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1001618208549"))
PRIVATE_LOG = int(os.environ.get("PRIVATE_LOG", "-1001660993748"))
force_subchannel = os.getenv("FSUB", "GalkoriyeDainamait")
OWNER_ID = int(os.environ.get("OWNER_ID", "1884885842"))
#Strings 
WELCOME_TEXT = "Hello.. <b>{}</b>\n<code>Type your query here..\nI'll respond to your query as earliest</code> 😉\n\nуσυ ωαииα тσ киσω αвσυт мє😌? яєα∂ вєℓσω\n\nαвσυт @Gishankrishka:-\n •му иαмє:- Gishan Krishka \n •му αgє:- υикиσωи🌝\n •¢σмρυтєя ℓαиgυαgє:- ωєв ∂єνєℓσρмєит(ℓєαяиιиg), ρутнσи мσяє ѕσσи😁\n•¢нє¢к [About ༒❣️☢️╣IrØή❂mคŇ╠☢️❣️༒](https://t.me/Gishankrishka_Info_bot) fσя мσяє\n\nPlz Don't Send Stickers 🥲\nReason :- [This](https://t.me/ultchat/19589)"
USER_DETAILS = "<b>PM FROM:</b>\nName: {} {}\nId: {}\nUname: @{}\nScam: {}\nRestricted: {}\nStatus: {}\nDc Id: {}"
PM_TXT_ATT = "<b>Message from:</b> {}\n<b>Name:</b> {}\n\n{}"
PM_TXT_ATTS = "<b>Message from:</b> {}\n<b>Name:</b> {}"
PM_MED_ATT = "<b>Message from:</b> {} \n<b>Name:</b> {}\n<b>Caption</b>:{}"
USER_DETAILS = "<b>FROM:</b>\nName: {} {}\nId: {}\nUname: @{}\nScam: {}\nRestricted: {}\nStatus: {}\nDc Id: {}"
FORCESUB_TEXT = "**❌ Access Denied ❌**\n\nYou Must Join Here\n♻️Join and Try Again.♻️"
HELP_STRING = "Meme Tiye nam dapam Mekata😒😂. Adminlata Msg Daanna One Nam ekat Mekata dapam 😒😂"
START_STRING ="""
Hi {}, Welcome to  Jollyathl Official Bot.
 Bot By [Charii 『🇱🇰』](https://t.me/Chari_x)
"""


#Inline Btn
FORCESUB_BUTTONS = InlineKeyboardMarkup([[
                 InlineKeyboardButton('Join Here', url=f"https://t.me/{force_subchannel}")
                 ],
                 [
                 InlineKeyboardButton('🐞 ʀᴘᴏʀᴛ ʙᴜɢs 🐞', user_id=f"@chari_x")
                 ],
                 [
                 InlineKeyboardButton(text="♻️ Reload ♻️",callback_data="ref")
                 ]]
                  )
                  
CLOSE_BUTTON = InlineKeyboardMarkup([[
                 InlineKeyboardButton("𝕮𝖑𝖔𝖒𝖘𝖊", callback_data="cloce")
                 ]]
                 )
                                                    
BACK_BUTTONS = InlineKeyboardMarkup([[
                 InlineKeyboardButton(text="👻 ʙᴀᴍᴄᴋ 👻",callback_data="bak")            
                 ]]
                  ) 

START_BUTTON = InlineKeyboardMarkup([[              
                 InlineKeyboardButton('🍁 Owner 🍁', user_id="@Chari_x")
                 ],
                 [
                 InlineKeyboardButton("➕ sʜᴀʀᴇ ➕", switch_inline_query="share"),
                 InlineKeyboardButton("➕ sʜᴀʀᴇ ᴄʜɴʟ ➕", switch_inline_query="cshare")
                 ],
                 [
                 InlineKeyboardButton("┊Memes 『🇱🇰』", url="https://t.me/GalkoriyeDainamait")
                 ]]
                  )



OWNER_BTN = InlineKeyboardMarkup([[              
                 InlineKeyboardButton('✨Owner✨', user_id="Chari_x")
                 ]]
                  )               



#Rndm Stkr

OWNER_STICKER = ["CAADAgADtA8AAhUWiEuTU2os6PSW-AI",
                "CAADAgADCwMAAm2wQgN_tBzazKZEJQI",
                "CAADBQADSwQAAnxrOFaYSIaXhBE_YAI"              
         ]

STAT_STICKER = ["CAADAgADtA8AAhUWiEuTU2os6PSW-AI"
                 
         ]  

HELP_STICKER = ["CAADAgADtA8AAhUWiEuTU2os6PSW-AI"
                
                              
         ]


#Menu Btn

start_menu = ReplyKeyboardMarkup(
      [
            ["✨Owner✨"]
          
           
        ],
        resize_keyboard=True  # Make the keyboard smaller
    )

next_1 = ReplyKeyboardMarkup(
      [
            ["BACK 🔙"]
           
        ],
        resize_keyboard=True  # Make the keyboard smaller
      )

back = ReplyKeyboardMarkup(
      [
            ["✨Owner✨"]
           
           
        ],
        resize_keyboard=True  # Make the keyboard smaller
      )     





print("Config Working....")
