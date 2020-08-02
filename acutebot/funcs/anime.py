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
)
from telegram.ext.dispatcher import run_async
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply

from acutebot import dp, typing, LOG
from acutebot.helpers import strings as st
from acutebot.helpers.parsedata import sort_caps
from acutebot.helpers.keyboard import keyboard

base_url = "https://kitsu.io/api/edge"


@run_async
@typing
def anime_entry(update, context):
    update.effective_message.reply_text(
        st.TOSEARCH_ANIME, reply_markup=ForceReply(selective=True),
    )

    return 1


@run_async
@typing
def anime(update, context):
    bot = context.bot
    msg = update.effective_message
    chat = update.effective_chat

    query = update.message.text
    query = query.replace(" ", "%20")

    res = r.get(f"{base_url}/anime?filter%5Btext%5D={query}")
    if res.status_code != 200:
        msg.reply_text(st.API_ERR)
        return -1

    res = res.json()["data"]
    if len(res) < 0:
        msg.reply_text(st.NOT_FOUND)
        return -1
    data = res[0]["attributes"]

    caption = st.ANIME_STR.format(
        data["titles"].get("en", ""),
        data["titles"].get("ja_jp", ""),
        data.get("subtype", "N/A"),
        data.get("ageRatingGuide", "N/A"),
        data.get("averageRating", "N/A"),
        data.get("status", "N/A"),
        data.get("startDate", "N/A"),
        data.get("endDate", "N/A"),
        data.get("episodeLength", "N/A"),
        data.get("episodeCount", "N/A"),
        data.get("synopsis", "N/A"),
    )

    try:
        if data.get("posterImage"):
            bot.sendPhoto(
                chat_id=chat.id,
                photo=data["posterImage"]["original"],
                caption=sort_caps(caption, c_id=res[0]["links"]["self"], anime=True),
                reply_markup=InlineKeyboardMarkup(
                    keyboard(
                        title=data.get("canonicalTitle"),
                        anime_ytkey=data.get("youtubeVideoId"),
                    )
                ),
                timeout=60,
                disable_web_page_preview=True,
            )

        else:
            bot.sendMessage(
                chat.id, text=caption, reply_markup=InlineKeyboardMarkup(keyboard())
            )

    except Exception as e:
        LOG.error(e)

    return ConversationHandler.END


@run_async
@typing
def cancel(update, context):
    context.bot.sendMessage(update.effective_chat.id, (st.CANCEL))
    return ConversationHandler.END


ANIME_HANDLER = ConversationHandler(
    entry_points=[CommandHandler("anime", anime_entry)],
    states={1: [MessageHandler(Filters.text & ~Filters.command, anime)]},
    fallbacks=[CommandHandler("cancel", cancel)],
    conversation_timeout=120,
)

dp.add_handler(ANIME_HANDLER)
