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
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

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
        text = "<b>🔖 Your watchlist:</b>\n\n"
        for title in fav:
            text += f"• {title.data}\n"
        keyb = [
            [InlineKeyboardButton(text="Watched ✅", callback_data=f"remfav_{user.id}")]
        ]
        msg.reply_text(text, reply_markup=InlineKeyboardMarkup(keyb))
    else:
        msg.reply_text(st.NOFAVS)


@run_async
def rem_favorite(update, context):
    query = update.callback_query
    user = update.effective_user
    user_id = query.data.split("_")[1]

    if user.id == int(user_id):
        sql.remove_fav(user_id)
        query.message.edit_text(st.REMFAV)
    else:
        query.answer(st.NOT_ALLOWED, show_alert=True)


LIST_FAV_HANDLER = CommandHandler("watchlist", list_favorite)
FAV_CLEAR_HANDLER = CallbackQueryHandler(rem_favorite, pattern=r"remfav_")
FAV_ADD_HANDLER = CallbackQueryHandler(add_favorite, pattern=r"addfav_")


dp.add_handler(LIST_FAV_HANDLER)
dp.add_handler(FAV_CLEAR_HANDLER)
dp.add_handler(FAV_ADD_HANDLER)
