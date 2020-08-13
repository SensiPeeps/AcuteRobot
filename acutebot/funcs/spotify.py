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
    spotify = SpotifyClient()
    if spotify.is_oauth_ready:
        url = spotify.auth_uri(state=user_id)
        msg.reply_text(
            st.SPT_LOGIN,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="Login", url=url)]]
            ),
        )

    else:
        msg.reply_text("Something went wrong! Please report to @starryboi")


def now_playing(update, context):
    user = update.effective_user
    chat = update.effective_chat
    msg = update.effective_message

    spt = get_spotify_data(user.id)
    if not spt:
        if chat.type == "private":
            return authorize(update, user.id)
        else:
            return msg.reply_text("contant in pm")

    music = spt.current_music
    if not music:
        music = spt.last_music

    msg.reply_text(f"{music.name}")


dp.add_handler(CommandHandler("nowplaying", now_playing))

