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


import os, lyricsgenius

from telegram.ext.dispatcher import run_async
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram.error import BadRequest
from telegram import ForceReply

from acutebot import dp, typing, LOG, GENIUS
from acutebot.helpers import strings as st

ARTIST, LYRICS = range(2)
SONGDICT = {}

if GENIUS is not None:
    genius = lyricsgenius.Genius(GENIUS)


@run_async
@typing
def songname(update, context):
    update.effective_message.reply_text(
        st.SONGNAME, reply_markup=ForceReply(selective=True)
    )

    return ARTIST


@run_async
@typing
def artistname(update, context):
    msg = update.effective_message
    user = update.effective_user
    song = update.message.text

    SONGDICT[user.id] = song
    msg.reply_text(st.ARTISTNAME, reply_markup=ForceReply(selective=True))

    return LYRICS


@run_async
@typing
def sendlyrics(update, context):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    artist = update.message.text

    try:
        song = SONGDICT[user.id]
    except KeyError:
        msg.reply_text(st.LYRICS_ERR)
        return -1
    rep = msg.reply_text("🔍 Looking for lyrics . . .")
    lyrics = genius.search_song(song, artist)
    if lyrics is None:
        msg.reply_text(st.LYRIC_NOT_FOUND)
        rep.delete()
        return -1
    try:
        msg.reply_text(f"🎸 <b>{song}</b> by <b>{artist}</b>:\n\n{lyrics.lyrics}")

    except BadRequest as excp:
        if excp.message == "Message is too long":
            msg.reply_text(st.LYRICS_TOO_BIG)
            with open("acute-lyrics.txt", "w+") as f:
                f.write(f"🎧 {song} by {artist}\n\n{lyrics.lyrics}")
            context.bot.sendDocument(
                chat_id=chat.id,
                document=open("acute-lyrics.txt", "rb"),
                caption=f"🎸 {song} - {artist}",
            )
            os.remove("acute-lyrics.txt")
        else:
            LOG.error(excp.message)

    rep.delete()
    del SONGDICT[user.id]
    return -1


@run_async
@typing
def cancel(update, context):
    context.bot.sendMessage(update.effective_chat.id, (st.CANCEL))
    return ConversationHandler.END


LYRICS_HANDLER = ConversationHandler(
    entry_points=[CommandHandler("lyrics", songname)],
    states={
        ARTIST: [MessageHandler(Filters.text & ~Filters.command, artistname)],
        LYRICS: [MessageHandler(Filters.text & ~Filters.command, sendlyrics)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
    conversation_timeout=120,
)

dp.add_handler(LYRICS_HANDLER)
