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

from acutebot import LOG, dp, cmd, updater, typing, DEV_ID
from acutebot.funcs import ALL_FUNCS
import acutebot.helpers.strings as st

from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext.dispatcher import run_async
from telegram.ext import PrefixHandler, Filters


# Import all funcs in main
for func_name in ALL_FUNCS:
    imported_module = importlib.import_module("acutebot.funcs." + func_name)


@run_async
@typing
def start(update, context):
    msg = update.effective_message
    if update.effective_chat.type == "private":
        msg.reply_text(
            st.START_STRING.format(update.effective_user.first_name),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Search Movies",
                            switch_inline_query_current_chat="<movie> ",
                        ),
                        InlineKeyboardButton(
                            text="Search TVshows",
                            switch_inline_query_current_chat="<tv> ",
                        ),
                    ]
                ]
            ),
        )
    else:
        msg.reply_text(st.START_STRING_GRP)


BANNER = r"""
  ___            ___     ______      ___
 / _ \           | |     | ___ \     | |
/ /_\ \ ___ _   _| |_ ___| |_/ / ___ | |_
|  _  |/ __| | | | __/ _ \ ___ \/ _ \| __|
| | | | (__| |_| | ||  __/ |_/ / (_) | |_
\_| |_/\___|\__,_|\__\___\____/ \___/ \__|

"""


def main():
    def stop_and_restart():
        updater.stop()
        os.execl(sys.executable, sys.executable, *sys.argv)

    def restart(update, context):
        update.effective_message.reply_text("Rebooted ✨")
        Thread(target=stop_and_restart).start()

    restart_handler = PrefixHandler(
        cmd, "reboot", restart, filters=Filters.user(DEV_ID)
    )
    start_handler = PrefixHandler(cmd, "start", start)

    dp.add_handler(restart_handler)
    dp.add_handler(start_handler)

    LOG.info(BANNER + "\nIs Running 🎶🎶🎵")
    updater.start_polling(timeout=15, read_latency=4)
    updater.idle()


if __name__ == "__main__":
    main()
