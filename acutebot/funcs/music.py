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


import os, deezloader, mutagen
from deezloader.exceptions import BadCredentials, TrackNotFound, NoDataApi

from pathlib import Path
from telegram.ext.dispatcher import run_async
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ForceReply, ReplyKeyboardMarkup
from pyrogram import Client

from acutebot import dp, typing, ARLTOKEN, LOG, APIID, APIHASH
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
    songq = update.message.text

    if songq in ("🎵 256KBs", "🎧 320KBs", "🎶 FLAC"):
        # save quality data in temp.dict:
        MUSICDICT[user.id] = {"q": songq}
        msg.reply_text(st.MUSICNAME, reply_markup=ForceReply(selective=True))
        return ARTIST
    msg.reply_text(st.INVALIDCAT)
    return -1


@run_async
@typing
def _artist(update, context):
    user = user = update.effective_user
    msg = update.effective_message
    musicn = update.message.text
    # update music title in dict:
    MUSICDICT[user.id]["mn"] = musicn
    msg.reply_text(st.ARTISTNAME, reply_markup=ForceReply(selective=True))
    return SENDMUSIC


@run_async
def sendmusic(update, context):
    user = update.effective_user
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

    try:
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
            duration = int(duration[0])

        if Path(file).stat().st_size < 50000000:
            rep = msg.reply_text(st.UPLOAD_BOTAPI)
            context.bot.sendAudio(
                chat.id,
                open(file, "rb"),
                caption="Via @acutebot 🎸",
                title=title,
                performer=artist,
                duration=duration,
                timeout=120,
            )
        else:
            rep = msg.reply_text(st.UPLOAD_MTPROTO)
            send_file_pyro(context.bot.token, file, chat.id, title, artist, duration)
        rep.delete()

    except Exception as e:
        LOG.error(e)

    if os.path.isfile(file):
        os.remove(file)
    del MUSICDICT[user.id]
    return ConversationHandler.END


def send_file_pyro(bot_token, file, chatid, title, artist, duration):
    bot = Client("acute", bot_token=bot_token, api_id=APIID, api_hash=APIHASH)
    with bot:
        bot.send_audio(
            chat_id=chatid,
            audio=open(file, "rb"),
            caption="Via @acutebot 🎸",
            title=title,
            duration=duration,
            performer=artist,
        )


@run_async
@typing
def cancel(update, context):
    context.bot.sendMessage(update.effective_chat.id, (st.CANCEL))
    return ConversationHandler.END


MUSIC_HANDLER = ConversationHandler(
    entry_points=[CommandHandler("music", musicq)],
    states={
        MUSIC: [MessageHandler(Filters.text & ~Filters.command, music)],
        ARTIST: [MessageHandler(Filters.text & ~Filters.command, _artist)],
        SENDMUSIC: [MessageHandler(Filters.text & ~Filters.command, sendmusic)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
    conversation_timeout=120,
)


dp.add_handler(MUSIC_HANDLER)
