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

from telegram.ext import InlineQueryHandler
from telegram.ext.dispatcher import run_async
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from acutebot import dp, TMDBAPI
from acutebot.helpers import strings as st
from acutebot.helpers.parsedata import article
from acutebot.helpers.keyboard import keyboard
from acutebot.helpers.database import users_sql as sql


pic_url = "https://image.tmdb.org/t/p"
base_url = "https://api.themoviedb.org/3"


@run_async
def inlinequery(update, context):
    query = update.inline_query.query
    sql.update_user(
        update.inline_query.from_user.id, update.inline_query.from_user.username
    )
    results = [][:50]
    if len(query) > 0:
        if query.startswith("<tv>"):
            query = query.replace("<tv>", "")
            res = r.get(
                f"{base_url}/search/tv?api_key={TMDBAPI}"
                + f"&language=en&query={query}"
                + "&page=1&include_adult=true"
            )

            if res.status_code != 200:
                return
            res = res.json()

            if len(res["results"]) > 0:
                for con in res["results"]:
                    results.append(
                        article(
                            title=con.get("name", "N/A"),
                            description=con.get("first_air_date", "N/A"),
                            thumb_url=f"{pic_url}/w500/{con['poster_path']}",
                            message_text=st.INLINE_STR.format(
                                con.get("original_name", "N/A"),
                                con.get("first_air_date", "N/A"),
                                con.get("popularity", "N/A"),
                                con.get("original_language", "N/A"),
                                con.get("vote_average", "N/A"),
                                con.get("overview", "N/A"),
                            )
                            + f"<a href='{pic_url}/w500/{con['poster_path']}'>&#xad</a>",
                            reply_markup=InlineKeyboardMarkup(
                                keyboard(title=con["original_name"], tv_id=con["id"])
                            ),
                        )
                    )

        elif query.startswith("<movie>"):
            query = query.replace("<movie>", "")
            res = r.get(
                f"{base_url}/search/movie?api_key={TMDBAPI}"
                + f"&language=en&query={query}"
                + "&page=1&include_adult=true"
            )

            if res.status_code != 200:
                return
            res = res.json()

            if len(res["results"]) > 0:
                for con in res["results"]:
                    results.append(
                        article(
                            title=con.get("title", "N/A"),
                            description=con.get("release_date", "N/A"),
                            thumb_url=f"{pic_url}/w500/{con['poster_path']}",
                            message_text=st.INLINE_STR.format(
                                con.get("original_title", "N/A"),
                                con.get("release_date", "N/A"),
                                con.get("popularity", "N/A"),
                                con.get("original_language", "N/A"),
                                con.get("vote_average", "N/A"),
                                con.get("overview", "N/A"),
                            )
                            + f"<a href='{pic_url}/w500/{con['poster_path']}'>&#xad</a>",
                            reply_markup=InlineKeyboardMarkup(
                                keyboard(title=con["original_title"], mv_id=con["id"])
                            ),
                        )
                    )

    else:
        results.append(
            article(
                title="Usage: <movie> or <tv> ",
                description="Example: <movie> Avengers endgame",
                message_text=st.INLINE_DESC,
                thumb_url="https://telegra.ph/file/292eb6f335bdb3b397806.jpg",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Search Movies",
                                switch_inline_query_current_chat="<movie> ",
                            ),
                            InlineKeyboardButton(
                                text="Search TVshows",
                                switch_inline_query_current_chat="<tv> ",
                            ),
                        ]
                    ]
                ),
            )
        )

    update.inline_query.answer(results, cache_time=10)


INLINE_HANDLER = InlineQueryHandler(inlinequery)
dp.add_handler(INLINE_HANDLER)
