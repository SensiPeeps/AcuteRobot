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



import deezloader
from deezloader.exceptions import BadCredentials, TrackNotFound

from os import remove
from telegram.ext.dispatcher import run_async
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ForceReply, ReplyKeyboardMarkup

from acutebot import dp, typing, ARLTOKEN
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
    reply_keyboard = [["🎧 320KBs", "🎶 FLAC"]]

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

    if musicq in ("🎧 320KBs", "🎶 FLAC"):
        # save quality data in temp.dict:
        MUSICDICT[user.id] = {"q": musicq, "mn": ""}
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

    rep = msg.reply_text("Uploading your music... 🎧")
    if quality == "🎧 320KBs":
        ql = "MP3_320"
    elif quality == "🎶 FLAC":
        ql = "FLAC"

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
    except TrackNotFound:
        msg.reply_text(st.MUSICNOTFOUND)
        rep.delete()
        return -1

    context.bot.sendAudio(chat.id, open(file, 'rb'), caption="By @acutebot 🎧", timeout=120)
    remove(file)
    rep.delete()
    return -1


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
