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

from acutebot import dp, TMDBAPI, typing
from acutebot.helpers import strings as st
from acutebot.helpers.parsedata import byname, byindex, sort_caps, tvruntime
from acutebot.helpers.keyboard import keyboard

base_url = "https://api.themoviedb.org/3"
pic_url = "https://image.tmdb.org/t/p"


def tvdata(c_id):
    """
    Parse TV shows data for the id and return class obj
    """
    payload = {"api_key": TMDBAPI, "language": "en-US", "append_to_response": "videos"}

    data = r.get(f"{base_url}/tv/{c_id}?", params=payload).json()

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
    msg = update.message
    user = update.effective_user
    query = msg.text.replace(" ", "%20")

    results = r.get(
        f"{base_url}/search/tv?api_key={TMDBAPI}"
        + f"&language=en&query={query}"
        + "&page=1&include_adult=true"
    )

    if results.status_code != 200:
        msg.reply_text(st.API_ERR)
        return -1

    results = results.json()["results"]

    if len(results) <= 0:
        msg.reply_text(st.NOT_FOUND)
        return -1

    keyb = []
    for x in results:
        keyb.append(
            [
                InlineKeyboardButton(
                    text=x.get("original_name"),
                    callback_data=f"tv_{x.get('id')}_{user.id}",
                )
            ]
        )
    msg.reply_text(
        f"🔍 Search results for <b>{msg.text}</b>:",
        reply_markup=InlineKeyboardMarkup(keyb[:6]),
    )

    return ConversationHandler.END


@run_async
def tv_button(update, context):
    query = update.callback_query
    chat = update.effective_chat
    user = update.effective_user

    spl = query.data.split("_")
    c_id, user_id = spl[1], spl[2]
    if user.id != int(user_id):
        return query.answer(st.NOT_ALLOWED, show_alert=True)

    query.answer("Hold on...")
    query.message.delete()

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

    if res.posterpath:
        context.bot.sendPhoto(
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
        context.bot.sendMessage(
            chat.id,
            text=caption,
            reply_markup=InlineKeyboardMarkup(
                keyboard(res.ytkey, res.homepage, res.title),
                disable_web_page_preview=True,
            ),
        )


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
TV_BUTTON_HANDLER = CallbackQueryHandler(tv_button, pattern=r"tv_")


dp.add_handler(TV_HANDLER)
dp.add_handler(TV_BUTTON_HANDLER)
