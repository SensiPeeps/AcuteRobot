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


from telegram.ext import InlineQueryHandler
from telegram.ext.dispatcher import run_async
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from acutebot import dp, LOG
from acutebot.helpers import strings as st
from acutebot.helpers.parsedata import article
from acutebot.helpers.keyboard import keyboard
from acutebot.helpers.getid import getid
from acutebot.funcs.movies import moviedata
from acutebot.funcs.tvseries import tvdata
from acutebot.helpers.database import users_sql as sql


pic_url = "https://image.tmdb.org/t/p"


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
            id = getid(query, type="TV")
            res = tvdata(id)
            try:
                results.append(
                    article(
                        title=res.title,
                        description=f"Created by : {res.creator}",
                        message_text=st.TV_STR.format(
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
                        + f"<a href='{pic_url}/w500/{res.posterpath}'>&#xad</a>",
                        thumb_url=f"{pic_url}/w500/{res.posterpath}",
                        reply_markup=InlineKeyboardMarkup(
                            keyboard(res.ytkey, res.homepage, res.title)
                        ),
                    )
                )
            except TypeError:
                pass
            except Exception as e:
                LOG.error(e)

        elif query.startswith("<movie>"):
            query = query.replace("<movie>", "")
            id = getid(query, type="MOVIE")
            res = moviedata(id)
            try:
                results.append(
                    article(
                        title=res.title,
                        description=res.tagline,
                        message_text=st.MOVIE_STR.format(
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
                        + f"<a href='{pic_url}/w500/{res.posterpath}'>&#xad</a>",
                        thumb_url=f"{pic_url}/w500/{res.posterpath}",
                        reply_markup=InlineKeyboardMarkup(
                            keyboard(res.ytkey, res.homepage, res.title, res.imdbid)
                        ),
                    )
                )
            except TypeError:
                pass
            except Exception as e:
                LOG.error(e)

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

    update.inline_query.answer(results)


INLINE_HANDLER = InlineQueryHandler(inlinequery)
dp.add_handler(INLINE_HANDLER)
