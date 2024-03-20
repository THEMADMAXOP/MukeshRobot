import random
import importlib
import re
import time
import asyncio
from platform import python_version as y
from sys import argv
from pyrogram import __version__ as pyrover
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram import __version__ as telever
from telegram.error import (
    BadRequest,
    ChatMigrated,
    NetworkError,
    TelegramError,
    TimedOut,
    Unauthorized,
)
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
)
from telegram.ext.dispatcher import DispatcherHandlerStop
from telegram.utils.helpers import escape_markdown
from telethon import __version__ as tlhver

import MukeshRobot.modules.no_sql.users_db as sql
from MukeshRobot import (
    BOT_NAME,
    BOT_USERNAME,
    LOGGER,
    OWNER_ID,
    START_IMG,
    SUPPORT_CHAT,
    TOKEN,
    StartTime,
    dispatcher,
    pbot,
    telethn,
    updater,
)
from MukeshRobot.modules import ALL_MODULES
from MukeshRobot.modules.helper_funcs.chat_status import is_user_admin
from MukeshRobot.modules.helper_funcs.misc import paginate_modules


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time
PM_START_TEX = """
❍ ʜᴇʟʟᴏ `{}`, ʜᴏᴡ ᴀʀᴇ ʏᴏᴜ \n❍ ʟᴏᴠᴇ ʏᴏᴜ ʙᴀʙʏ... 
"""


PM_START_TEXT = """ 
*❍ ʜᴇʏ {}, ᴡᴇʟᴄᴏᴍᴇ ʙᴀʙʏ* !\n━━━━━━━━━━━━━━━━━━━━━━\n\n❍ *ɪ ᴀᴍ {}, ᴀɴᴅ ɪ ʜᴀᴠᴇ sᴘᴇᴄɪᴀʟ ғᴇᴀᴛᴜʀᴇs.*\n\n❍ *ᴜsᴇʀs ➛ {}*\n❍ *ᴄʜᴀᴛs ➛ {}*\n\n❍ *ɪ ʜᴀᴠᴇ ᴍᴏsᴛ ᴘᴏᴡᴇʀғᴜʟʟ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ + ᴍᴜsɪᴄ ʙᴏᴛ ғᴇᴀᴛᴜʀᴇs.*"""

buttons = [
    [
        InlineKeyboardButton(
            text=" ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ ", 
            url=f"https://t.me/{dispatcher.bot.username}?startgroup=true", 
        ),
    ],
    [
        InlineKeyboardButton(text="sᴜᴘᴘᴏʀᴛ", url="HTTPS://T.ME/VOICEOFHEART0"),
        InlineKeyboardButton(text="ᴀʙᴏᴜᴛ", callback_data="mukesh_"),
    ],
    [
        InlineKeyboardButton(text="ʜᴇʟᴘ ᴄᴏᴍᴍᴀɴᴅs", callback_data="Main_help"),
    ],
     
]


roy = [
    [
        InlineKeyboardButton(text="ᴜᴘᴅᴀᴛᴇ", url=f"https://t.me/STATUSDAIRY2"),
        InlineKeyboardButton(text="ꜱᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_CHAT}"),
    ],
    [
        InlineKeyboardButton(
            text="ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ",
            url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
        ),
    ],
]

HELP_STRINGS = f"""
❍ *{BOT_NAME}  ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟʟᴏᴡ ᴛᴏ ɢᴇᴛ ᴅᴇsᴄʀɪᴘᴛɪᴏɴ ᴀʙᴏᴜᴛ sᴘᴇᴄɪғɪᴄs ᴄᴏᴍᴍᴀɴᴅ*"""

ABHI = [
"https://graph.org/file/f76fd86d1936d45a63c64.jpg",
"https://graph.org/file/69ba894371860cd22d92e.jpg",
"https://graph.org/file/67fde88d8c3aa8327d363.jpg",
"https://graph.org/file/3a400f1f32fc381913061.jpg",
"https://graph.org/file/a0893f3a1e6777f6de821.jpg",
"https://graph.org/file/5a285fc0124657c7b7a0b.jpg",
"https://graph.org/file/25e215c4602b241b66829.jpg",
"https://graph.org/file/a13e9733afdad69720d67.jpg",
"https://graph.org/file/692e89f8fe20554e7a139.jpg",
"https://graph.org/file/db277a7810a3f65d92f22.jpg",
"https://graph.org/file/a00f89c5aa75735896e0f.jpg",
"https://graph.org/file/f86b71018196c5cfe7344.jpg",
"https://graph.org/file/a3db9af88f25bb1b99325.jpg",
"https://graph.org/file/5b344a55f3d5199b63fa5.jpg",
"https://graph.org/file/84de4b440300297a8ecb3.jpg",
"https://graph.org/file/84e84ff778b045879d24f.jpg",
"https://graph.org/file/a4a8f0e5c0e6b18249ffc.jpg",
"https://graph.org/file/ed92cada78099c9c3a4f7.jpg",
"https://graph.org/file/d6360613d0fa7a9d2f90b.jpg",
"https://graph.org/file/37248e7bdff70c662a702.jpg",
"https://graph.org/file/0bfe29d15e918917d1305.jpg",
"https://graph.org/file/16b1a2828cc507f8048bd.jpg",
"https://graph.org/file/e6b01f23f2871e128dad8.jpg",
"https://graph.org/file/cacbdddee77784d9ed2b7.jpg",
"https://graph.org/file/ddc5d6ec1c33276507b19.jpg",
"https://graph.org/file/39d7277189360d2c85b62.jpg",
"https://graph.org/file/5846b9214eaf12c3ed100.jpg",
"https://graph.org/file/ad4f9beb4d526e6615e18.jpg",
"https://graph.org/file/3514efaabe774e4f181f2.jpg",   

]

NYKAA = [
    "https://graph.org/file/9bba2b7ee9ba3806de65d.jpg",
    "https://graph.org/file/ef82f289043a4fa74f8ff.jpg",
    "https://graph.org/file/9c27c68958e06ae074c38.jpg",
    "https://graph.org/file/0ff325b1d2efe80299aa3.jpg",
    "https://graph.org/file/41167b953cf3579853d47.jpg",
    "https://graph.org/file/bd93ab42e69305f274028.jpg",
    "https://graph.org/file/97575db5586c05d6b2898.jpg",
    "https://graph.org/file/07c393fdf931a407c9bc0.jpg",
    "https://graph.org/file/f332767490ad3a5ca20e8.jpg",
    "https://graph.org/file/f3449e9069667f647d14e.jpg",
    "https://graph.org/file/9f51cdc739f907cbd2c7e.jpg",
    "https://telegra.ph/file/d7a6a923c38e051ce35f3.jpg",
    "https://graph.org/file/f86b71018196c5cfe7344.jpg",
    "https://graph.org/file/a3db9af88f25bb1b99325.jpg",
    "https://graph.org/file/5b344a55f3d5199b63fa5.jpg",
    "https://graph.org/file/84de4b440300297a8ecb3.jpg",
    "https://graph.org/file/84e84ff778b045879d24f.jpg",
    "https://graph.org/file/a4a8f0e5c0e6b18249ffc.jpg",
    "https://graph.org/file/ed92cada78099c9c3a4f7.jpg",
    "https://graph.org/file/d6360613d0fa7a9d2f90b.jpg",
    "https://graph.org/file/37248e7bdff70c662a702.jpg",
    "https://graph.org/file/0bfe29d15e918917d1305.jpg",
    "https://graph.org/file/16b1a2828cc507f8048bd.jpg",
    "https://graph.org/file/e6b01f23f2871e128dad8.jpg",
    "https://graph.org/file/cacbdddee77784d9ed2b7.jpg",
    "https://graph.org/file/ddc5d6ec1c33276507b19.jpg",
    "https://graph.org/file/39d7277189360d2c85b62.jpg",
    "https://graph.org/file/5846b9214eaf12c3ed100.jpg",
    "https://graph.org/file/ad4f9beb4d526e6615e18.jpg",
    "https://graph.org/file/3514efaabe774e4f181f2.jpg",    
]


DONATE_STRING = f"""❍ ʜᴇʏ ʙᴀʙʏ, ʜᴀᴩᴩʏ ᴛᴏ ʜᴇᴀʀ ᴛʜᴀᴛ ʏᴏᴜ ᴡᴀɴɴᴀ ᴅᴏɴᴀᴛᴇ. ʏᴏᴜ ᴄᴀɴ ᴅɪʀᴇᴄᴛʟʏ ᴄᴏɴᴛᴀᴄᴛ ᴍʏ ᴅᴇᴠᴇʟᴏᴘᴇʀ @ABOUT_SASHIKANT ғᴏʀ ᴅᴏɴᴀᴛɪɴɢ ᴏʀ ʏᴏᴜ ᴄᴀɴ ᴠɪsɪᴛ ᴍʏ sᴜᴩᴩᴏʀᴛ ᴄʜᴀᴛ @VOICEOFHEART0 ᴀɴᴅ ᴀsᴋ ᴛʜᴇʀᴇ ᴀʙᴏᴜᴛ ᴅᴏɴᴀᴛɪᴏɴ."""

IMPORTED = {}
MIGRATEABLE = []
HELPABLE = {}
STATS = []
USER_INFO = []
DATA_IMPORT = []
DATA_EXPORT = []
CHAT_SETTINGS = {}
USER_SETTINGS = {}

for module_name in ALL_MODULES:
    imported_module = importlib.import_module("MukeshRobot.modules." + module_name)
    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__

    if imported_module.__mod_name__.lower() not in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception("Can't have two modules with the same name! Please change one")

    if hasattr(imported_module, "__help__") and imported_module.__help__:
        HELPABLE[imported_module.__mod_name__.lower()] = imported_module

    # Chats to migrate on chat_migrated events
    if hasattr(imported_module, "__migrate__"):
        MIGRATEABLE.append(imported_module)

    if hasattr(imported_module, "__stats__"):
        STATS.append(imported_module)

    if hasattr(imported_module, "__user_info__"):
        USER_INFO.append(imported_module)

    if hasattr(imported_module, "__import_data__"):
        DATA_IMPORT.append(imported_module)

    if hasattr(imported_module, "__export_data__"):
        DATA_EXPORT.append(imported_module)

    if hasattr(imported_module, "__chat_settings__"):
        CHAT_SETTINGS[imported_module.__mod_name__.lower()] = imported_module

    if hasattr(imported_module, "__user_settings__"):
        USER_SETTINGS[imported_module.__mod_name__.lower()] = imported_module


# do not async
def send_help(chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    dispatcher.bot.send_photo(
        chat_id=chat_id,
        photo=START_IMG,
        caption=text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=keyboard,
    )

def start(update: Update, context: CallbackContext):
    args = context.args
    global uptime
    uptime = get_readable_time((time.time() - StartTime))
    if update.effective_chat.type == "private":
        if len(args) >= 1:
            if args[0].lower() == "help":
                send_help(update.effective_chat.id, HELP_STRINGS)
            elif args[0].lower().startswith("ghelp_"):
                mod = args[0].lower().split("_", 1)[1]
                if not HELPABLE.get(mod, False):
                    return
                send_help(
                    update.effective_chat.id,
                    HELPABLE[mod].__help__,
                    InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="◁", callback_data="help_back")]]
                    ),
                )
            elif args[0].lower() == "markdownhelp":
                IMPORTED["exᴛʀᴀs"].markdown_help_sender(update)
            elif args[0].lower().startswith("stngs_"):
                match = re.match("stngs_(.*)", args[0].lower())
                chat = dispatcher.bot.getChat(match.group(1))

                if is_user_admin(chat, update.effective_user.id):
                    send_settings(match.group(1), update.effective_user.id, False)
                else:
                    send_settings(match.group(1), update.effective_user.id, True)

            elif args[0][1:].isdigit() and "rᴜʟᴇs" in IMPORTED:
                IMPORTED["rᴜʟᴇs"].send_rules(update, args[0], from_pm=True)

        else:
            first_name = update.effective_user.first_name
            
            x=update.effective_message.reply_sticker(
                "CAACAgUAAxkBAAI33mLYLNLilbRI-sKAAob0P7koTEJNAAIOBAACl42QVKnra4sdzC_uKQQ")
            x.delete()
            usr = update.effective_user
            lol = update.effective_message.reply_text(
                PM_START_TEX.format(usr.first_name), parse_mode=ParseMode.MARKDOWN
            )
            time.sleep(0.4)
            lol.edit_text("💛")
            time.sleep(0.5)
            lol.edit_text("🤍")
            time.sleep(0.3)
            lol.edit_text("❤️")
            time.sleep(0.4)
            lol.delete()
            
            update.effective_message.reply_photo(random.choice(NYKAA),PM_START_TEXT.format(escape_markdown(first_name),BOT_NAME,sql.num_users(),sql.num_chats()),
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=ParseMode.MARKDOWN,
                timeout=60,
            )
    else:
        update.effective_message.reply_photo(
            random.choice(NYKAA),
            caption="❍ ɪ ᴀᴍ ᴀʟɪᴠᴇ ʙᴀʙʏ...!\n\n❍ <b>ɪ ᴅɪᴅɴ'ᴛ sʟᴇᴘᴛ ʙᴀʙʏ.</b> \n\n❍ ᴜᴘᴛɪᴍᴇ ➛ <code>{}</code>".format(
                uptime
            ),
            reply_markup=InlineKeyboardMarkup(roy),
            parse_mode=ParseMode.HTML,
        )


def error_handler(update, context):
    """๏ ʟᴏɢ ᴛʜᴇ ᴇʀʀᴏʀ ᴀɴᴅ sᴇɴᴅ ᴀ ᴛᴇʟᴇɢʀᴀᴍ ᴍᴇssᴀɢᴇ ᴛᴏ ɴᴏᴛɪғʏ ᴛʜᴇ ᴅᴇᴠᴇʟᴏᴘᴇʀ."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    LOGGER.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    message = (
        "❍ ᴀɴ ᴇxᴄᴇᴘᴛɪᴏɴ ᴡᴀs ʀᴀɪsᴇᴅ ᴡʜɪʟᴇ ʜᴀɴᴅʟɪɴɢ ᴀɴ ᴜᴘᴅᴀᴛᴇ\n"
        "❍ <pre>ᴜᴘᴅᴀᴛᴇ = {}</pre>\n\n"
        "❍ <pre>{}</pre>"
    ).format(
        html.escape(json.dumps(update.to_dict(), indent=2, ensure_ascii=False)),
        html.escape(tb),
    )

    if len(message) >= 4096:
        message = message[:4096]
    # Finally, send the message
    context.bot.send_message(chat_id=OWNER_ID, text=message, parse_mode=ParseMode.HTML)


# for test purposes
def error_callback(update: Update, context: CallbackContext):
    error = context.error
    try:
        raise error
    except Unauthorized:
        print("no nono1")
        print(error)
        # remove update.message.chat_id from conversation list
    except BadRequest:
        print("no nono2")
        print("BadRequest caught")
        print(error)

        # handle malformed requests - read more below!
    except TimedOut:
        print("no nono3")
        # handle slow connection problems
    except NetworkError:
        print("no nono4")
        # handle other connection problems
    except ChatMigrated as err:
        print("no nono5")
        print(err)
        # the chat_id of a group has changed, use e.new_chat_id instead
    except TelegramError:
        print(error)
        # handle all other telegram related errors


def help_button(update, context):
    query = update.callback_query
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)

    print(query.message.chat.id)

    try:
        if mod_match:
            module = mod_match.group(1)
            text = (
                "❅ *ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅs ꜰᴏʀ* *{}* ❅\n".format(
                    HELPABLE[module].__mod_name__
                )
                + HELPABLE[module].__help__
            )
            query.message.edit_caption(text,
                parse_mode=ParseMode.MARKDOWN,
                
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="ʙᴀᴄᴋ", callback_data="help_back"),InlineKeyboardButton(text="sᴜᴘᴘᴏʀᴛ", callback_data="mukesh_support")]]
                ),
            )

        elif prev_match:
            curr_page = int(prev_match.group(1))
            query.message.edit_caption(HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(curr_page - 1, HELPABLE, "help")
                ),
            )

        elif next_match:
            next_page = int(next_match.group(1))
            query.message.edit_caption(HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(next_page + 1, HELPABLE, "help")
                ),
            )

        elif back_match:
            query.message.edit_caption(HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, HELPABLE, "help")
                ),
            )

        # ensure no spinny white circle
        context.bot.answer_callback_query(query.id)
        # query.message.delete()

    except BadRequest:
        pass


def Mukesh_about_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "mukesh_":
        uptime = get_readable_time((time.time() - StartTime))
        query.message.edit_caption(f"*✦ ɪ ᴀᴍ {dispatcher.bot.first_name} ✦*"
            "\n\n*❍ ɪ ʜᴀᴠᴇ ᴍᴏsᴛ ᴘᴏᴡᴇʀғᴜʟʟ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ + ᴍᴜsɪᴄ ʙᴏᴛ ғᴇᴀᴛᴜʀᴇs.*"
            "\n\n*❍ ᴡʀɪᴛᴛᴇɴ ɪɴ ᴩʏᴛʜᴏɴ ᴡɪᴛʜ sǫʟᴀʟᴄʜᴇᴍʏ ᴀɴᴅ ᴍᴏɴɢᴏᴅʙ ᴀs ᴅᴀᴛᴀʙᴀsᴇ.*"
            f"\n\n*❍ ᴜsᴇʀs ➛* {sql.num_users()}"
            f"\n*❍ ᴄʜᴀᴛs ➛* {sql.num_chats()}"
            "\n\n❍ ɪ ᴄᴀɴ ʀᴇꜱᴛʀɪᴄᴛ ᴜꜱᴇʀꜱ."
            "\n❍ ɪ ʜᴀᴠᴇ ᴀɴ ᴀᴅᴠᴀɴᴄᴇᴅ ᴀɴᴛɪ-ꜰʟᴏᴏᴅ ꜱʏꜱᴛᴇᴍ."
            "\n❍ ᴀᴅᴠᴀɴᴄᴇ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ᴄᴀᴘᴀʙɪʟɪᴛʏ."
            "\n❍ ᴀɴɪᴍᴇ ʙᴏᴛ ғᴜɴᴄᴛɪᴏɴᴀʟɪᴛʏ."
            "\n❍ ᴀɪ ɪɴᴛᴇɢʀᴀᴛɪᴏɴ."
            f"\n\n❍ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ɢɪᴠᴇɴ ʙᴇʟᴏᴡ ғᴏʀ ɢᴇᴛᴛɪɴɢ ʙᴀsɪᴄ ʜᴇʟᴩ ᴀɴᴅ ɪɴғᴏ ᴀʙᴏᴜᴛ {dispatcher.bot.first_name}.",
            parse_mode=ParseMode.MARKDOWN,
                                   
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="ʜᴇʟᴘ ᴍᴇɴᴜ", callback_data="Main_help"
                        ),
                        InlineKeyboardButton(text="ᴜᴘᴅᴀᴛᴇ", url="https://t.me/STATUSDAIRY2"),
                    ],
                    [
                        InlineKeyboardButton(text="ʜᴏᴍᴇ", callback_data="mukesh_back"),
                    ],
                ]
            ),
            )
    elif query.data == "mukesh_support":
        query.message.edit_caption("**❍ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ɢɪᴠᴇɴ ʙᴜᴛᴛᴏɴ ᴛᴏ ᴊᴏɪɴ ᴏᴜʀ ɢʀᴏᴜᴘ ᴀɴᴅ ᴄʜᴀɴɴᴇʟ ᴛᴏ ʙᴏᴛ ᴜᴘᴅᴀᴛᴇ ɪɴғᴏʀᴍᴀᴛɪᴏɴ.**"
            f"\n\n❍ ɪғ ᴀɴʏ ʙᴜɢ ɪɴ {dispatcher.bot.first_name}, ᴩʟᴇᴀsᴇ ʀᴇᴩᴏʀᴛ ɪᴛ ᴀᴛ sᴜᴩᴩᴏʀᴛ ᴄʜᴀᴛ.",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="ꜱᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_CHAT}"
                        ),
                        InlineKeyboardButton(
                            text="ᴜᴘᴅᴀᴛᴇ", url=f"https://t.me/STATUSDAIRY2"
                        ),
                    ],
                    [
                        InlineKeyboardButton(text="ʜᴏᴍᴇ", callback_data="mukesh_back"),
                    ],
                ]
            ),
        )
    elif query.data == "mukesh_back":
        first_name = update.effective_user.first_name 
        query.message.edit_caption(PM_START_TEXT.format(escape_markdown(first_name), BOT_NAME,sql.num_users(),sql.num_chats()),
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.MARKDOWN,
            timeout=60,
        )
def MukeshRobot_Main_Callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "Main_help":
        query.message.edit_caption(f"""
 ✦ ʜᴇʀᴇ ɪꜱ ʜᴇʟᴘ ᴍᴇɴᴜ ꜰᴏʀ {BOT_NAME}
""",
            parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="ᴍᴀɴᴀɢᴇ", callback_data="help_back"),
                        InlineKeyboardButton(text="ᴍᴜsɪᴄ", callback_data="Music_")
                    ],
                    [
                        InlineKeyboardButton(text="ʜᴏᴍᴇ", callback_data="mukesh_back")
                    ],
                ]
            ),
            )
    elif query.data=="basic_help":
        query.message.edit_caption("""✿ ʜᴇʀᴇ ɪs ᴀʟʟ ᴀɴɪᴍᴇ ʀᴀɴᴅᴏᴍ ɪᴍɢᴇs ᴄᴏᴍᴍᴀɴᴅs.\n\n❍ /gecg ➛ sᴇɴᴅ ʀᴀɴᴅᴏᴍ ɢᴇᴄɢ ɪᴍɢ.\n❍ /avatar ➛ sᴇɴᴅs ʀᴀɴᴅᴏᴍ ᴀᴠᴀᴛᴀʀ ɪᴍɢ.\n❍ /foxgirl ➛ sᴇɴᴅs ʀᴀɴᴅᴏᴍ ғᴏxɢɪʀʟ sᴏᴜʀᴄᴇ ɪᴍᴀɢᴇs.\n❍ /waifus ➛ sᴇɴᴅs ʀᴀɴᴅᴏᴍ ᴡᴀɪғᴜ ɪᴍɢ.\n❍ /neko ➛ sᴇɴᴅs ʀᴀɴᴅᴏᴍ sғᴡ ɴᴇᴋᴏ sᴏᴜʀᴄᴇ ɪᴍᴀɢᴇs.\n❍ /gasm ➛ sᴇɴᴅs ʀᴀɴᴅᴏᴍ ᴏʀɢᴀsᴍ ɪᴍɢ.\n❍ /cuddle ➛ sᴇɴᴅs ʀᴀɴᴅᴏᴍ ᴄᴜᴅᴅʟᴇ ɪᴍɢ.\n❍ /shinobu ➛ sᴇɴᴅ ʀᴀɴᴅᴏᴍ sʜɪɴᴏʙᴜ ɪᴍɢ.\n❍ /megumin ➛ sᴇɴᴅ ʀᴀɴᴅᴏᴍ ᴍᴇɢᴜᴍɪɴ ɪᴍɢ.\n❍ /bully ➛ sᴇɴᴅ ʀᴀɴᴅᴏᴍ ʙᴜʟʟʏ ɪᴍɢ.\n❍ /cry ➛ sᴇɴᴅ ʀᴀɴᴅᴏᴍ ᴄʀʏ ɪᴍɢ.\n❍ /awoo ➛ sᴇɴᴅ ʀᴀɴᴅᴏᴍ ᴀᴡᴏᴏ ɪᴍɢ.""",parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="ʙᴀᴄᴋ", callback_data="Main_help"),InlineKeyboardButton(text="ANIME", callback_data="Avisha_")
                    ]
                ]
            ),
            )
    elif query.data=="mukesh_back":
        query.message.edit_caption("""✿ ᴇxᴘᴇʀᴛ ᴄᴏᴍᴍᴀɴᴅs ✿

❅ ᴀᴠᴀɪʟᴀʙʟᴇ ᴛᴏ ᴀᴅᴍɪɴs ❅

❍  /unbanall ➛ ᴍᴇᴍʙᴇʀs ғʀᴏᴍ ʏᴏᴜʀ ɢʀᴏᴜᴘs
❍  /unmuteall ➛ ᴜɴᴍᴜᴛᴇᴀʟʟ ᴀʟʟ ғʀᴏᴍ ʏᴏᴜʀ ɢʀᴏᴜᴘ

❅ ᴘɪɴɴᴇᴅ Mᴇssᴀɢᴇs ❅

❍  /pin ➛ [ᴍᴇssᴀɢᴇ] sᴇɴᴅs ᴛʜᴇ ᴍᴇssᴀɢᴇ ᴛʜʀᴏᴜɢʜ ᴛʜᴇ ʙᴏᴛ ᴀɴᴅ ᴘɪɴs ɪᴛ.
❍  /pin ➛ ᴘɪɴs ᴛʜᴇ ᴍᴇssᴀɢᴇ ɪɴ ʀᴇᴘʟʏ
❍  /unpin ➛ ʀᴇᴍᴏᴠᴇs ᴛʜᴇ ᴘɪɴɴᴇᴅ ᴍᴇs
