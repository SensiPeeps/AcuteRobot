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


import os, sys, importlib
from threading import Thread

from acutebot import LOG, dp, updater, DEV_ID
from acutebot.funcs import ALL_FUNCS
import acutebot.helpers.strings as st


from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext.dispatcher import run_async
from telegram.ext import CommandHandler, CallbackQueryHandler, Filters


# Import all funcs in main
for func_name in ALL_FUNCS:
    imported_module = importlib.import_module("acutebot.funcs." + func_name)


class Starter:
    def __init__(self, name):
        self.photo = "https://telegra.ph/file/7d76172f26f7f3c6d2f9a.jpg"
        self.text = st.START_STRING.format(name)
        self.reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Movie", switch_inline_query_current_chat="<movie> ",
                    ),
                    InlineKeyboardButton(
                        text="TVshow", switch_inline_query_current_chat="<tv> ",
                    ),
                    InlineKeyboardButton(
                        text="Anime", switch_inline_query_current_chat="<anime> ",
                    ),
                ],
                [InlineKeyboardButton(text="🐾  About me  🐾", callback_data="about")],
                [InlineKeyboardButton(text="Help and Commands❔", callback_data="help")],
            ]
        )


@run_async
def start(update, context):
    if update.effective_chat.type == "private":
        stuff = Starter(update.effective_user.first_name)
        return update.effective_message.reply_photo(
            photo=stuff.photo, caption=stuff.text, reply_markup=stuff.reply_markup
        )

    update.effective_message.reply_text(st.START_STRING_GRP)


@run_async
def about_button(update, context):
    query = update.callback_query
    query.answer()
    query.message.edit_caption(
        caption=st.ABOUT_STR,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Github 🔭", url="https://github.com/starry69"
                    ),
                    InlineKeyboardButton(text="Donate 🖤", url="paypal.me/starryrays"),
                ],
                [InlineKeyboardButton(text="Go back 🔙", callback_data="back_btn")],
            ]
        ),
    )


@run_async
def help_button(update, context):
    query = update.callback_query
    query.answer()
    query.message.edit_caption(
        caption=st.HELP_STR,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Go back 🔙", callback_data="back_btn")]]
        ),
    )


@run_async
def back_btn(update, context):
    query = update.callback_query
    query.answer()
    stuff = Starter(update.effective_user.first_name)
    query.message.edit_caption(caption=stuff.text, reply_markup=stuff.reply_markup)


BANNER = r"""
  ___            ___     ______      ___
 / _ \           | |     | ___ \     | |
/ /_\ \ ___ _   _| |_ ___| |_/ / ___ | |_
|  _  |/ __| | | | __/ _ \ ___ \/ _ \| __|
| | | | (__| |_| | ||  __/ |_/ / (_) | |_
\_| |_/\___|\__,_|\__\___\____/ \___/ \__|

Is Running 🎶🎶🎵
"""


def main():
    def stop_and_restart():
        updater.stop()
        os.execl(sys.executable, sys.executable, *sys.argv)

    def restart(update, context):
        context.bot.sendMessage(update.effective_chat.id, "Rebooted ✨")
        Thread(target=stop_and_restart).start()

    restart_handler = CommandHandler("reboot", restart, filters=Filters.user(DEV_ID))
    start_handler = CommandHandler("start", start)
    about_handler = CallbackQueryHandler(about_button, pattern=r"about")
    help_handler = CallbackQueryHandler(help_button, pattern=r"help")
    back_btn_handler = CallbackQueryHandler(back_btn, pattern=r"back_btn")

    dp.add_handler(restart_handler)
    dp.add_handler(start_handler)
    dp.add_handler(about_handler)
    dp.add_handler(help_handler)
    dp.add_handler(back_btn_handler)

    LOG.info("%s", BANNER)

    # Start the bot.
    updater.start_polling(timeout=15, read_latency=4)
    updater.idle()


if __name__ == "__main__":
    main()
