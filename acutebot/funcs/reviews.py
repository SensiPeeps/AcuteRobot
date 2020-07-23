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

from telegram.ext.dispatcher import run_async
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply

from acutebot import dp, TMDBAPI, typing
from acutebot.helpers import strings as st
from acutebot.helpers.getid import getid
from acutebot.helpers.parsedata import sort_text

NAME, TV, MOVIE = range(3)
base_url = "https://api.themoviedb.org/3"


@run_async
@typing
def review_entry(update, context):
    reply_keyboard = [["TV series", "Movies"]]

    update.effective_message.reply_text(
        st.TOSEARCHREVIEW,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, selective=True
        ),
    )

    return NAME


@run_async
@typing
def name(update, context):
    msg = update.message
    name = msg.text
    if name == "TV series":
        msg.reply_text(st.TOSEARCHTV, reply_markup=ForceReply(force_reply=True))
        return TV
    elif name == "Movies":
        msg.reply_text(st.TOSEARCHMOVIE, reply_markup=ForceReply(force_reply=True))
        return MOVIE
    else:
        msg.reply_text(st.INVALIDREVIEWNAME, reply_markup=ReplyKeyboardRemove())
        return -1


@run_async
@typing
def tvreview(update, context):
    msg = update.message
    id = getid(msg.text, type="TV")

    if id == "api_error":
        msg.reply_text(st.API_ERR)
        return -1

    elif id == "not_found":
        msg.reply_text(st.NOT_FOUND)
        return -1

    try:
        res = r.get(
            f"{base_url}/tv/{id}/reviews?api_key={TMDBAPI}&language=en&page=1"
        ).json()

        text = reviewdata(res, msg.text)
        msg.reply_text(text, reply_markup=ReplyKeyboardRemove())

    finally:
        return -1


@run_async
@typing
def moviereview(update, context):
    msg = update.message
    id = getid(msg.text, type="MOVIE")

    if id == "api_error":
        msg.reply_text(st.API_ERR)
        return -1
    elif id == "not_found":
        msg.reply_text(st.NOT_FOUND)
        return -1

    try:
        res = r.get(
            f"{base_url}/movie/{id}/reviews?api_key={TMDBAPI}&language=en&page=1"
        ).json()

        text = reviewdata(res, msg.text)
        msg.reply_text(text, reply_markup=ReplyKeyboardRemove())

    finally:
        return -1


def reviewdata(res: dict, title: str):
    """build review text from dict"""

    results = res["results"]
    author = []
    content = []

    if len(results) > 0:
        for dic in results:
            author.append(dic["author"])
            content.append(dic["content"])
    else:
        return st.REVIEW_NOT_FOUND

    text = f"💬 Reviews for <b>{title}</b>\n\n"
    num = 0
    loop = 0
    for a in author:
        if loop < 2:  # we only want 2 reviews
            text += f"<b>☃️ By {a}</b> :\n"
            for c in content:
                text += f"<em>{content[num]}</em>\n\n"
                num += 1
                break
            loop += 1
        else:
            break
    return sort_text(text)


@run_async
def cancel(update, context):
    update.effective_message.reply_text(st.CANCEL)
    return ConversationHandler.END



REVIEW_HANDLER = ConversationHandler(
    entry_points=[CommandHandler("reviews", review_entry)],
    states={
        NAME: [MessageHandler(Filters.text & ~Filters.command, name)],
        TV: [MessageHandler(Filters.text & ~Filters.command, tvreview)],
        MOVIE: [MessageHandler(Filters.text & ~Filters.command, moviereview)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

dp.add_handler(REVIEW_HANDLER)
