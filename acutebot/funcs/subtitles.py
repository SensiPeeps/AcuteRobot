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
from io import BytesIO

from telegram.ext import (
    MessageHandler,
    CommandHandler,
    CallbackQueryHandler,
    Filters,
    ConversationHandler,
)

from telegram.ext.dispatcher import run_async
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply

from acutebot import dp, typing
from acutebot.helpers import strings as st

base_url = "http://subtitle.iamidiotareyoutoo.com"


@run_async
@typing
def subs_entry(update, context):

    update.effective_message.reply_text(
        st.TOSEARCHSUBS, reply_markup=ForceReply(selective=True),
    )

    return 1


@run_async
@typing
def getsubs(update, context):
    msg = update.effective_message
    text = update.message.text
    query = text.replace(" ", "%20")

    res = r.get(f"{base_url}/search/{query}/1").json()
    resarr = res.get("r")
    if len(resarr) <= 0:
        msg.reply_text(st.NOT_FOUND)
        return -1

    keyb = []
    for x in resarr:
        keyb.append(
            [
                InlineKeyboardButton(
                    text=x.get("SIQ"), callback_data=f"subs_{x.get('DMCA_ID')}"
                )
            ]
        )
    msg.reply_text(st.SUBS_STR.format(text), reply_markup=InlineKeyboardMarkup(keyb))
    return ConversationHandler.END


@run_async
def subsbutton(update, context):
    query = update.callback_query
    chat = update.effective_chat
    query.answer()
    tm = query.message.reply_text("⌛ Hold on . . .")
    query.message.delete()

    subs_id = query.data.split("_")[1]
    res = r.get(f"{base_url}/get/{subs_id}/").json()
    dl_link = base_url + res.get("DL_LINK")
    dl_content_name = res.get("DL_SUB_NAME")

    dl_content = BytesIO(r.get(dl_link).content)
    dl_content.name = dl_content_name
    context.bot.sendDocument(chat.id, dl_content, caption="Subtitle via @acutebot 🎸")
    tm.delete()


@run_async
@typing
def cancel(update, context):
    context.bot.sendMessage(update.effective_chat.id, (st.CANCEL))
    return ConversationHandler.END


SUBS_HANDLER = ConversationHandler(
    entry_points=[CommandHandler("subtitle", subs_entry)],
    states={1: [MessageHandler(Filters.text & ~Filters.command, getsubs)]},
    fallbacks=[CommandHandler("cancel", cancel)],
    conversation_timeout=120,
)

SUBS_CALLBACK_HANDLER = CallbackQueryHandler(subsbutton, pattern=r"subs_")


dp.add_handler(SUBS_HANDLER)
dp.add_handler(SUBS_CALLBACK_HANDLER)
