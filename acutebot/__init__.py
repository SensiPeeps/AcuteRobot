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


import logging
import os
import sys
from functools import wraps
from telegram.ext import Updater, Defaults
from telegram import ChatAction, ParseMode

ENV = bool(os.environ.get("ENV", False))
if ENV:
    TOKEN = os.environ.get("TOKEN")
    TMDBAPI = os.environ.get("TMDBAPI")
    DB_URI = os.environ.get("DATABASE_URL")
    GENIUS = os.environ.get("GENIUS")
    DEBUG = bool(os.environ.get("DEBUG", False))
    ARLTOKEN = os.environ.get("ARL")
    APIID = os.environ.get("APIID")
    APIHASH = os.environ.get("APIHASH")


else:
    from acutebot.config import Config

    TOKEN = Config.TOKEN
    TMDBAPI = Config.TMDBAPI
    DB_URI = Config.DB_URI
    GENIUS = Config.GENIUS
    DEBUG = Config.DEBUG
    ARLTOKEN = Config.ARL
    APIID = Config.APIID
    APIHASH = Config.APIHASH

if DEBUG:
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.DEBUG,
    )
else:
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

__version__ = "1.0.7-rev08"

DEV_ID = 894380120
LOG = logging.getLogger(__name__)

# Check python version:
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOG.info("You MUST need to have python version 3.6! shutting down...")
    quit(1)


def typing(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(
            chat_id=update.effective_chat.id, action=ChatAction.TYPING
        )
        return func(update, context, *args, **kwargs)

    return command_func


# Use HTML treewide;
defaults = Defaults(parse_mode=ParseMode.HTML)

updater = Updater(TOKEN, use_context=True, defaults=defaults)
dp = updater.dispatcher
