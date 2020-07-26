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


import lyricsgenius

from os import remove
from telegram.ext.dispatcher import run_async
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ForceReply

from acutebot import dp, typing, GENIUS
from acutebot.helpers import strings as st

ARTIST, LYRICS = range(2)
SONGDICT = {}

if GENIUS is not None:
    genius = lyricsgenius.Genius(GENIUS)


@run_async
@typing
def songname(update, context):
    update.effective_message.reply_text(
        st.SONGNAME, reply_markup=ForceReply(force_reply=True, selective=True)
    )

    return ARTIST


@run_async
@typing
def artistname(update, context):
    msg = update.effective_message
    user = update.effective_user
    song = update.message.text

    SONGDICT[user.id] = song
    msg.reply_text(st.ARTISTNAME, reply_markup=ForceReply(force_reply=True, selective=True))

    return LYRICS


@run_async
@typing
def lyrics(update, context):
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
    if len(lyrics.lyrics) > 4096:
        msg.reply_text(st.LYRICS_TOO_BIG)
        with open("acute-lyrics.txt", "w+") as f:
            f.write(f"🎧 {song} by {artist}\n\n{lyrics.lyrics}")
        context.bot.sendDocument(
            chat_id=chat.id, document=open("acute-lyrics.txt", "rb")
        )
        remove("acute-lyrics.txt")
    else:
        msg.reply_text(f"🎧 <b>{song}</b> by <b>{artist}</b>: "
                       f"\n\n{lyrics.lyrics}")
    rep.delete()
    return -1


@run_async
@typing
def cancel(update, context):
    update.effective_message.reply_text(st.CANCEL)
    return ConversationHandler.END


LYRICS_HANDLER = ConversationHandler(
    entry_points=[CommandHandler("lyrics", songname)],
    states={
        ARTIST: [MessageHandler(Filters.text & ~Filters.command, artistname)],
        LYRICS: [MessageHandler(Filters.text & ~Filters.command, lyrics)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

dp.add_handler(LYRICS_HANDLER)
