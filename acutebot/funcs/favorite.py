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



from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram.ext.dispatcher import run_async

from acutebot import dp, typing
import acutebot.helpers.strings as st
import acutebot.helpers.database.favorites_sql as sql


@run_async
def add_favorite(update, context):
    query = update.callback_query
    userid = update.effective_user.id
    match = query.data.split("_")[1]

    add = sql.add_fav(userid, match)
    if add:
       query.answer(st.SAVED_FAV.format(match), show_alert=True)
    else:
       query.answer(st.FAV_EXIST, show_alert=True)


@run_async
@typing
def list_favorite(update, context):
    msg = update.effective_message
    user = update.effective_user
    fav = sql.get_fav(user.id)
    if fav:
       text = "🎬 Your watchlist:\n\n"
       for title in fav:
           text += f"• {title.data}\n"
       msg.reply_text(text)
    else:
       msg.reply_text(st.NOFAVS)


@run_async
@typing
def rem_favorite(update, context):
    msg = update.effective_message
    user = update.effective_user
    rem = sql.remove_fav(user.id)
    if rem:
       msg.reply_text(st.REMFAV)
    else:
       msg.reply_text(st.NOFAVS)


LIST_FAV_HANDLER = CommandHandler("watchlist", list_favorite)
FAV_CLEAR_HANDLER = CommandHandler("clearlist", rem_favorite)
FAV_CALLBACK_HANDLER = CallbackQueryHandler(add_favorite, pattern=r"fav_")


dp.add_handler(LIST_FAV_HANDLER)
dp.add_handler(FAV_CLEAR_HANDLER)
dp.add_handler(FAV_CALLBACK_HANDLER)
