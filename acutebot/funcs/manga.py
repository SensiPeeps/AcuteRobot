#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# MIT License
# Copyright (c) 2020 Stɑrry Shivɑm // This file is part of AcuteBot
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import requests as r

from telegram.ext import (
    MessageHandler,
    CommandHandler,
    Filters,
    ConversationHandler,
    CallbackQueryHandler,
)

from telegram.ext.dispatcher import run_async
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply

from acutebot import dp, typing
from acutebot.helpers import strings as st
from acutebot.helpers.parsedata import sort_caps
from acutebot.helpers.keyboard import keyboard

base_url = "https://kitsu.io/api/edge"
tempdict = {}


@run_async
@typing
def manga_entry(update, context):
    update.effective_message.reply_text(
        st.TOSEARCH_MANGA, reply_markup=ForceReply(selective=True),
    )

    return 1


@run_async
@typing
def manga(update, context):
    msg = update.message
    user = update.effective_user
    query = msg.text.replace(" ", "%20")

    res = r.get(f"{base_url}/manga?filter%5Btext%5D={query}")
    if res.status_code != 200:
        msg.reply_text(st.API_ERR)
        return -1

    res = res.json()["data"]
    if len(res) <= 0:
        msg.reply_text(st.NOT_FOUND)
        return -1

    # Add results array with user's id as key
    tempdict[user.id] = res

    keyb = []
    for x in enumerate(res):
        titles = x[1]["attributes"]["titles"]
        keyb.append(
            [
                InlineKeyboardButton(
                    text=f"{titles.get('en') if titles.get('en') else titles.get('ja_jp')}",
                    callback_data=f"manga_{x[0]}_{user.id}",
                )
            ]
        )

    msg.reply_text(
        f"🔍 Search results for <b>{msg.text}</b>:",
        reply_markup=InlineKeyboardMarkup(keyb[:6]),
    )

    return ConversationHandler.END


@run_async
def manga_button(update, context):
    query = update.callback_query
    chat = update.effective_chat
    user = update.effective_user

    spl = query.data.split("_")
    x, user_id = int(spl[1]), int(spl[2])
    if user.id != user_id:
        return query.answer(st.NOT_ALLOWED, show_alert=True)

    try:
        res = tempdict[user_id]
    except KeyError:
        return query.answer(st.KEYERROR, show_alert=True)

    query.answer("Hold on...")
    query.message.delete()

    data = res[x]["attributes"]
    caption = st.MANGA_STR.format(
        data["titles"].get("en", ""),
        data["titles"].get("ja_jp", ""),
        data.get("subtype", "N/A"),
        data.get("averageRating", "N/A"),
        data.get("status", "N/A"),
        data.get("startDate", "N/A"),
        data.get("endDate", "N/A"),
        data.get("volumeCount", "N/A"),
        data.get("chapterCount", "N/A"),
        data.get("serialization", "N/A"),
        data.get("synopsis", "N/A"),
    )

    if data.get("posterImage"):
        context.bot.sendPhoto(
            chat_id=chat.id,
            photo=data["posterImage"]["original"],
            caption=sort_caps(caption, c_id=data["slug"], manga=True),
            reply_markup=InlineKeyboardMarkup(keyboard(manga_id=data["slug"],)),
            timeout=60,
            disable_web_page_preview=True,
        )

    else:
        context.bot.sendMessage(
            chat.id,
            text=caption,
            reply_markup=InlineKeyboardMarkup(keyboard(manga_id=data["slug"],)),
            disable_web_page_preview=True,
        )
    del tempdict[user_id]


@run_async
@typing
def cancel(update, context):
    context.bot.sendMessage(update.effective_chat.id, (st.CANCEL))
    return ConversationHandler.END


MANGA_HANDLER = ConversationHandler(
    entry_points=[CommandHandler("manga", manga_entry)],
    states={1: [MessageHandler(Filters.text & ~Filters.command, manga)]},
    fallbacks=[CommandHandler("cancel", cancel)],
    conversation_timeout=120,
)
MANGA_BUTTON_HANDLER = CallbackQueryHandler(manga_button, pattern=r"manga_")

dp.add_handler(MANGA_HANDLER)
dp.add_handler(MANGA_BUTTON_HANDLER)
