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

import asyncio
import deezloader, mutagen
from deezloader.exceptions import BadCredentials, TrackNotFound, NoDataApi

from pathlib import Path
from os import remove
from telegram.ext.dispatcher import run_async
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ForceReply, ReplyKeyboardMarkup
from telethon import TelegramClient

from acutebot import dp, typing, ARLTOKEN, APIID, APIHASH
from acutebot.helpers import strings as st

MUSIC, ARTIST, SENDMUSIC = range(3)
MUSICDICT = {}

if ARLTOKEN is not None:
    try:
        downloa = deezloader.Login(ARLTOKEN)
    except BadCredentials:
        print("Deezer token is dead :(")


@run_async
@typing
def musicq(update, context):
    reply_keyboard = [["🎵 256KBs", "🎧 320KBs", "🎶 FLAC"]]

    update.effective_message.reply_text(
        st.MUSICQ,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, selective=True
        ),
    )
    return MUSIC


@run_async
@typing
def music(update, context):
    user = update.effective_user
    msg = update.effective_message
    musicq = update.message.text

    if musicq in ("🎵 256KBs", "🎧 320KBs", "🎶 FLAC"):
        # save quality data in temp.dict:
        MUSICDICT[user.id] = {"q": musicq}
        msg.reply_text(
            st.MUSICNAME, reply_markup=ForceReply(force_reply=True, selective=True)
        )
        return ARTIST
    msg.reply_text(st.INVALIDREVIEWNAME)
    return -1


@run_async
@typing
def artist(update, context):
    user = user = update.effective_user
    msg = update.effective_message
    musicn = update.message.text
    # update music title in dict:
    MUSICDICT[user.id]["mn"] = musicn
    msg.reply_text(
        st.ARTISTNAME, reply_markup=ForceReply(force_reply=True, selective=True)
    )
    return SENDMUSIC


@run_async
@typing
def sendmusic(update, context):
    user = user = update.effective_user
    msg = update.effective_message
    chat = update.effective_chat

    artist = update.message.text
    try:
        song = MUSICDICT[user.id]["mn"]
        quality = MUSICDICT[user.id]["q"]
    except KeyError:
        msg.reply_text(st.LYRICS_ERR)
        return -1

    if quality == "🎧 320KBs":
        ql = "MP3_320"
    elif quality == "🎶 FLAC":
        ql = "FLAC"
    elif quality == "🎵 256KBs":
        ql = "MP3_256"

    try:
        context.bot.send_chat_action(chat.id, "upload_document")
        file = downloa.download_name(
            artist=artist,
            song=song,
            output="temp",
            quality=ql,
            recursive_quality=True,
            recursive_download=True,
            not_interface=True,
        )
    except (TrackNotFound, NoDataApi):
        msg.reply_text(st.MUSICNOTFOUND)
        return -1

    # Fetch correct details from metadata:
    aud = mutagen.File(file)
    title = aud.get("title")
    if title:
       title = str(title[0])
    artist = aud.get("artist")
    if artist:
       artist = str(artist[0])
    duration = aud.get("length")
    if duration:
       duration = str(duration[0])

    if Path(file).stat().st_size < 50000000:
        rep = msg.reply_text(st.UPLOAD_BOTAPI)
        context.bot.sendAudio(
            chat.id,
            open(file, "rb"),
            caption="Via @acutebot 🎧",
            title=title,
            performer=artist,
            duration=duration,
            timeout=120,
        )
    else:
        rep = msg.reply_text(st.UPLOAD_TELETHON)
        loop = asyncio.new_event_loop()
        send_file_telethon(context.bot.token, file, chat.id, loop)
    remove(file)
    rep.delete()
    return -1


def send_file_telethon(bot_token, file, chatid, loop):
    api_id = APIID
    api_hash = APIHASH
    bot = TelegramClient("acute", api_id, api_hash, loop=loop).start(
        bot_token=bot_token
    )
    with bot:
       loop.run_until_complete(bot.send_file(chatid, open(file, "rb")))


@run_async
@typing
def cancel(update, context):
    update.effective_message.reply_text(st.CANCEL)
    return ConversationHandler.END


MUSIC_HANDLER = ConversationHandler(
    entry_points=[CommandHandler("music", musicq)],
    states={
        MUSIC: [MessageHandler(Filters.text & ~Filters.command, music)],
        ARTIST: [MessageHandler(Filters.text & ~Filters.command, artist)],
        SENDMUSIC: [MessageHandler(Filters.text & ~Filters.command, sendmusic)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)


dp.add_handler(MUSIC_HANDLER)
