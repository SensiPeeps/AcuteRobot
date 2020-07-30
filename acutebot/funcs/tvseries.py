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
from telegram import InlineKeyboardMarkup, ForceReply

from acutebot import dp, LOG, TMDBAPI, typing
from acutebot.helpers import strings as st
from acutebot.helpers.parsedata import byname, byindex, sort_caps, tvruntime
from acutebot.helpers.keyboard import keyboard
from acutebot.helpers.getid import getid

base_url = "https://api.themoviedb.org/3"
pic_url = "https://image.tmdb.org/t/p"


def tvdata(c_id):
    """
    Parse TV shows data for the id and return class obj
    """

    data = r.get(
        f"{base_url}/tv/{c_id}?api_key={TMDBAPI}"
        + "&language=en"
        + "&append_to_response=videos"
    ).json()

    class res:

        c_id = data.get("id")
        title = data.get("original_name")
        creator = byindex(data.get("created_by"))
        genres = byname(data.get("genres"))
        language = data.get("original_language")
        runtime = tvruntime(data.get("episode_run_time"))
        faired = data.get("first_air_date")
        laired = data.get("last_air_date")
        status = data.get("status")
        seasons = data.get("number_of_seasons")
        numeps = data.get("number_of_episodes")
        rating = data.get("vote_average")
        company = byindex(data.get("production_companies"))
        overview = data.get("overview")

        # Keyboard objects
        posterpath = data.get("poster_path")
        homepage = data.get("homepage")
        ytkey = data.get("videos")

    return res


@run_async
@typing
def tv_entry(update, context):

    update.effective_message.reply_text(
        st.TOSEARCHTV, reply_markup=ForceReply(selective=True),
    )

    return 1


@run_async
@typing
def tv(update, context):
    bot = context.bot
    msg = update.message
    chat = update.effective_chat

    c_id = getid(msg.text, category="TV")

    if c_id == "api_error":
        msg.reply_text(st.API_ERR)
        return -1

    if c_id == "not_found":
        msg.reply_text(st.NOT_FOUND)
        return -1

    res = tvdata(c_id)
    caption = st.TV_STR.format(
        res.title,
        res.creator,
        res.genres,
        res.language,
        res.runtime,
        res.faired,
        res.laired,
        res.status,
        res.seasons,
        res.numeps,
        res.rating,
        res.company,
        res.overview,
    )

    try:
        if res.posterpath:
            bot.sendPhoto(
                chat_id=chat.id,
                photo=f"{pic_url}/w500/{res.posterpath}",
                caption=sort_caps(caption, c_id=res.c_id, tv=True),
                reply_markup=InlineKeyboardMarkup(
                    keyboard(res.ytkey, res.homepage, res.title)
                ),
                disable_web_page_preview=True,
                timeout=60,
            )
        else:
            bot.sendMessage(
                chat.id,
                text=caption,
                reply_markup=InlineKeyboardMarkup(
                    keyboard(res.ytkey, res.homepage, res.title),
                    disable_web_page_preview=True,
                ),
            )

    except Exception as e:
        LOG.error(e)

    return ConversationHandler.END


@run_async
@typing
def cancel(update, context):
    context.bot.sendMessage(update.effective_chat.id, (st.CANCEL))
    return ConversationHandler.END


TV_HANDLER = ConversationHandler(
    entry_points=[CommandHandler("tvshows", tv_entry)],
    states={1: [MessageHandler(Filters.text & ~Filters.command, tv)]},
    fallbacks=[CommandHandler("cancel", cancel)],
    conversation_timeout=120,
)


dp.add_handler(TV_HANDLER)

