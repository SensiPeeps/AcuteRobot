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
from acutebot.helpers.parsedata import byname, currency, sort_caps
from acutebot.helpers.keyboard import keyboard


base_url = "https://api.themoviedb.org/3"
pic_url = "https://image.tmdb.org/t/p"


def moviedata(c_id):
    """
    Parse movie data for the id and return class obj
    """
    payload = {"api_key": TMDBAPI, "language": "en-US", "append_to_response": "videos"}

    data = r.get(f"{base_url}/movie/{c_id}?", params=payload).json()

    class res:

        c_id = data.get("id")
        title = data.get("title")
        tagline = data.get("tagline")
        status = data.get("status")
        genres = byname(data.get("genres"))
        language = byname(data.get("spoken_languages"))
        runtime = data.get("runtime")
        budget = currency(data.get("budget"))
        revenue = currency(data.get("revenue"))
        release = data.get("release_date")
        rating = data.get("vote_average")
        popularity = data.get("popularity")
        overview = data.get("overview")

        # Keyboard objects
        posterpath = data.get("poster_path")
        homepage = data.get("homepage")
        imdbid = data.get("imdb_id")
        ytkey = data.get("videos")

    return res


@run_async
@typing
def movie_entry(update, context):

    update.effective_message.reply_text(
        st.TOSEARCHMOVIE, reply_markup=ForceReply(selective=True),
    )

    return 1


@run_async
@typing
def movie(update, context):
    msg = update.message
    user = update.effective_user
    query = msg.text.replace(" ", "%20")

    results = r.get(
        f"{base_url}/search/movie?api_key={TMDBAPI}"
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
                    text=x.get("title"), callback_data=f"movie_{x.get('id')}_{user.id}"
                )
            ]
        )
    msg.reply_text(
        f"🔍 Search results for <b>{msg.text}</b>:",
        reply_markup=InlineKeyboardMarkup(keyb[:6]),
    )

    return ConversationHandler.END


@run_async
def movie_button(update, context):
    query = update.callback_query
    chat = update.effective_chat
    user = update.effective_user

    spl = query.data.split("_")
    c_id, user_id = spl[1], spl[2]
    if user.id != int(user_id):
        return query.answer(st.NOT_ALLOWED, show_alert=True)

    query.answer("Hold on...")
    query.message.delete()

    res = moviedata(c_id)
    caption = st.MOVIE_STR.format(
        res.title,
        res.tagline,
        res.status,
        res.genres,
        res.language,
        res.runtime,
        res.budget,
        res.revenue,
        res.release,
        res.rating,
        res.popularity,
        res.overview,
    )

    if res.posterpath:
        context.bot.sendPhoto(
            chat_id=chat.id,
            photo=f"{pic_url}/w500/{res.posterpath}",
            caption=sort_caps(caption, c_id=res.c_id, mv=True),
            reply_markup=InlineKeyboardMarkup(
                keyboard(res.ytkey, res.homepage, res.title, res.imdbid)
            ),
            timeout=60,
            disable_web_page_preview=True,
        )
    else:
        context.bot.sendMessage(
            chat.id,
            text=caption,
            reply_markup=InlineKeyboardMarkup(
                keyboard(res.ytkey, res.homepage, res.title, res.imdbid),
                disable_web_page_preview=True,
            ),
        )


@run_async
@typing
def cancel(update, context):
    context.bot.sendMessage(update.effective_chat.id, (st.CANCEL))
    return ConversationHandler.END


MOVIE_HANDLER = ConversationHandler(
    entry_points=[CommandHandler("movies", movie_entry)],
    states={1: [MessageHandler(Filters.text & ~Filters.command, movie)]},
    fallbacks=[CommandHandler("cancel", cancel)],
    conversation_timeout=120,
)
MV_BUTTON_HANDLER = CallbackQueryHandler(movie_button, pattern=r"movie_")

dp.add_handler(MOVIE_HANDLER)
dp.add_handler(MV_BUTTON_HANDLER)
