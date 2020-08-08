from saucenao_api import SauceNao, VideoSauce
from saucenao_api.params import DB, Hide, BgColor
from saucenao_api.errors import (
    BadFileSizeError,
    ShortLimitReachedError,
    LongLimitReachedError,
    UnknownServerError,
    UnknownClientError,
)

from telegram.ext import CommandHandler
from telegram.ext.dispatcher import run_async
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from acutebot import dp, typing, SAUCEAPI
from acutebot.helpers import strings as st

if SAUCEAPI:
    sauce = SauceNao(api_key=SAUCEAPI, db=DB.ALL, hide=Hide.NONE, bgcolor=BgColor.WHITE)


LOOKUP_STR = """
• Similarity : {} %
• Title : {}
• Author : {}
"""
IF_VID = """
• Est time : {}
• Year {}
"""


def saucekeyb(results):
    num = 0
    keyb = []
    for x in results:
        if not x.url:
            break
        num += 1
        keyb.append([InlineKeyboardButton(text=f"🔍 Source {num}", url=x.url)])
    return keyb


@run_async
@typing
def lookup(update, context):
    msg = update.effective_message
    bot = context.bot
    file_id = None

    if msg.reply_to_message:
        if msg.reply_to_message.sticker:
            if msg.reply_to_message.sticker.is_animated:
                return msg.reply_text(st.WRONG_FILE)
            file_id = msg.reply_to_message.sticker.file_id

        elif msg.reply_to_message.photo:
            file_id = msg.reply_to_message.photo[-1].file_id
        elif msg.reply_to_message.document:
            file_id = msg.reply_to_message.document.file_id
        elif msg.reply_to_message.animation:
            file_id = msg.reply_to_message.animation.file_id
        else:
            return msg.reply_text(st.WRONG_FILE)

        file_url = bot.get_file(file_id)["file_path"]
        tmsg = msg.reply_text("🔍 Searching . . .")

        try:
            results = sauce.from_url(file_url)
            thumb = results[0].thumbnail
            similarity = results[0].similarity
            title = results[0].title
            author = results[0].author
            print(results.short_remaining)
            print(results.long_remaining)

            text = LOOKUP_STR.format(similarity, title, author)
            if isinstance(results[0], VideoSauce):
                year = results[0].year
                esttime = results[0].est_time
                text += IF_VID.format(esttime, year)

            msg.reply_photo(
                thumb, text, reply_markup=InlineKeyboardMarkup(saucekeyb(results))
            )

        # Catch all exceptions:
        except (IndexError, UnknownClientError, UnknownServerError):
            return tmsg.edit_text(st.NOT_FOUND)
        except BadFileSizeError:
            return tmsg.edit_text(st.BAD_FILE)
        except ShortLimitReachedError:
            return tmsg.edit_text(st.S_LIMIT)
        except LongLimitReachedError:
            return tmsg.edit_text(st.L_LIMIT)
    else:
        msg.reply_text(st.LOOKUP_NOREPLY)


LOOKUP_HANDLER = CommandHandler("lookup", lookup)
dp.add_handler(LOOKUP_HANDLER)
