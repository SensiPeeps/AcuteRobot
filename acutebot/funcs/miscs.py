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


import requests as r
import subprocess, random
from time import sleep

from acutebot.helpers.database import users_sql as sql
from acutebot.helpers.database.favorites_sql import fav_count
import acutebot.helpers.strings as st
from acutebot import dp, typing, DEV_ID, LOG

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, TelegramError
from telegram.ext.dispatcher import run_async
from telegram.ext import CommandHandler, MessageHandler, Filters
from telegram.error import BadRequest


@run_async
@typing
def get_ip(update, context):
    res = r.get("http://ipinfo.io/ip")
    update.message.reply_text(res.text)


@run_async
def rmemes(update, context):
    msg = update.effective_message
    chat = update.effective_chat

    SUBREDS = [
        "meirl",
        "dankmemes",
        "AdviceAnimals",
        "memes",
        "meme",
        "memes_of_the_dank",
        "PornhubComments",
        "teenagers",
        "memesIRL",
        "insanepeoplefacebook",
        "terriblefacebookmemes",
        "animememes",
        "Animemes",
        "memeeconomy",
    ]

    subreddit = random.choice(SUBREDS)
    res = r.get(f"https://meme-api.herokuapp.com/gimme/{subreddit}")

    if res.status_code != 200:  # Like if api is down?
        return msg.reply_text(st.API_ERR)
    res = res.json()

    keyb = [[InlineKeyboardButton(text=f"r/{res['subreddit']}", url=res["postLink"])]]
    try:
        context.bot.send_chat_action(chat.id, "upload_photo")
        context.bot.send_photo(
            chat.id,
            photo=res["url"],
            caption=(res["title"]),
            reply_markup=InlineKeyboardMarkup(keyb),
            timeout=60,
        )

    except BadRequest as excp:
        LOG.error(excp)


@run_async
def stats(update, context):
    msg = update.effective_message
    return msg.reply_text(
        st.STATS.format(sql.users_count(), fav_count()), parse_mode=None,
    )


@run_async
def greet(update, context):
    msg = update.effective_message
    user = update.effective_user
    chat = update.effective_chat

    new_members = msg.new_chat_members
    for new_mem in new_members:
        if new_mem.id == context.bot.id:
            msg.reply_text(st.GREET.format(user.first_name, chat.title))


@run_async
def shell(update, context):
    bot = context.bot
    msg = update.effective_message
    chat = update.effective_chat
    command = " ".join(context.args).split()
    rep = msg.reply_text("Running command...")
    try:
        res = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,)
        stdout, stderr = res.communicate()
        result = str(stdout.decode().strip()) + str(stderr.decode().strip())
        bot.editMessageText("<pre>" + result + "</pre>", chat.id, rep.message_id)
    except Exception as e:
        bot.editMessageText(str(e), chat.id, rep.message_id)


@run_async
def broadcast(update, context):
    to_send = update.effective_message.text.split(None, 1)
    if len(to_send) >= 2:
        users = sql.get_all_users() or []
        failed = 0
        for user in users:
            try:
                context.bot.sendMessage(int(user.user_id), to_send[1])
                sleep(0.1)
            except TelegramError:
                failed += 1
                LOG.warning(
                    "Couldn't send broadcast to %s, username %s",
                    str(user.user_id),
                    str(user.username),
                )

        update.effective_message.reply_text(
            "Broadcast complete. {} users failed to receive the message, probably "
            "due to being Blocked.".format(failed)
        )



@run_async
def log_user(update, context):
    msg = update.effective_message

    sql.update_user(msg.from_user.id, msg.from_user.username)

    if msg.reply_to_message:
        sql.update_user(
            msg.reply_to_message.from_user.id, msg.reply_to_message.from_user.username,
        )

    if msg.forward_from:
        sql.update_user(msg.forward_from.id, msg.forward_from.username)


IP_HANDLER = CommandHandler("ip", get_ip, filters=Filters.chat(DEV_ID))
REDDIT_HANDLER = CommandHandler("reddit", rmemes)
STATS_HANDLER = CommandHandler("stats", stats, filters=Filters.user(DEV_ID))
GREET_HANDLER = MessageHandler(Filters.status_update.new_chat_members, greet)
SHELL_HANDLER = CommandHandler("shell", shell, filters=Filters.user(DEV_ID))
LOG_HANDLER = MessageHandler(Filters.all, log_user)
BROADCAST_HANDLER = CommandHandler(
    "broadcast", broadcast, filters=Filters.user(DEV_ID)
)

dp.add_handler(IP_HANDLER)
dp.add_handler(REDDIT_HANDLER)
dp.add_handler(STATS_HANDLER)
dp.add_handler(GREET_HANDLER)
dp.add_handler(SHELL_HANDLER)
dp.add_handler(LOG_HANDLER, 1)
dp.add_handler(BROADCAST_HANDLER)
