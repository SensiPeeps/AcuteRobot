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


from telegram.ext import CommandHandler
from telegram.ext.dispatcher import run_async
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from acutebot import dp, typing
from acutebot.helpers.spthelper import SpotifyClient, get_spotify_data
import acutebot.helpers.strings as st


def authorize(update, user_id):
    msg = update.effective_message
    user = update.effective_user
    spotify = SpotifyClient()
    if spotify.is_oauth_ready:
        url = spotify.auth_uri(state=user_id)
        msg.reply_text(
            st.SPT_LOGIN.format(user.first_name),
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="Authorize", url=url)]]
            ),
        )

    else:
        msg.reply_text("Something went wrong! Please report to @starryboi")


@run_async
@typing
def now_playing(update, context):
    user = update.effective_user
    chat = update.effective_chat
    msg = update.effective_message

    spt = get_spotify_data(user.id)
    if not spt:
        if chat.type == "private":
            return authorize(update, user.id)
        return msg.reply_text(st.SPT_LOGIN_PM)

    text = ""
    music = spt.current_music
    if music:
        text = f"<b>{user.first_name} is currently listening to</b>"
    else:
        music = spt.last_music
        text = f"<b>{user.first_name} was listening to</b>"

    text += f" <a href='{music.url}'>{music.name}</a> by <b>{music.artist}</b>"
    msg.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Open in spotify", url=music.url)]]
        ),
    )


dp.add_handler(CommandHandler("nowplaying", now_playing))
