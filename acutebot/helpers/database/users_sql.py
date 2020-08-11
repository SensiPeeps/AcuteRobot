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


import threading

from sqlalchemy import Column, Integer, UnicodeText
from acutebot.helpers.database import SESSION, BASE
from acutebot import dp


class Users(BASE):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    username = Column(UnicodeText)

    def __init__(self, user_id, username=None):
        self.user_id = user_id
        self.username = username

    def __repr__(self):
        return "<User {} ({})>".format(self.username, self.user_id)


Users.__table__.create(checkfirst=True)
INSERTION_LOCK = threading.RLock()


def ensure_bot_in_db():
    with INSERTION_LOCK:
        bot = Users(dp.bot.id, dp.bot.username)
        SESSION.merge(bot)
        SESSION.commit()


def update_user(user_id, username):
    with INSERTION_LOCK:
        user = SESSION.query(Users).get(user_id)
        if not user:
            user = Users(user_id, username)
            SESSION.add(user)
            SESSION.flush()
        else:
            user.username = username
        SESSION.commit()


ensure_bot_in_db()


def users_count():
    try:
        return SESSION.query(Users).count()
    finally:
        SESSION.close()
