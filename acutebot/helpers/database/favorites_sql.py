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
from acutebot.helpers.database import SESSION, BASE
from sqlalchemy import Column, UnicodeText, Numeric


class Favourites(BASE):
    __tablename__ = "favourites"
    user_id = Column(Numeric, primary_key=True)
    data = Column(UnicodeText, primary_key=True)

    def __init__(self, user_id, data):
        self.user_id = user_id
        self.data = data


Favourites.__table__.create(checkfirst=True)
FAV_INSERTION_LOCK = threading.RLock()

def check_fav(user_id, data):
    try:
        return SESSION.query(Favourites).get((int(user_id), str(data)))
    finally:
        SESSION.close()


def get_fav(user_id):
    try:
        return SESSION.query(Favourites).filter(
            Favourites.user_id == int(user_id)).all()
    finally:
        SESSION.close()


def add_fav(user_id, data):
    with FAV_INSERTION_LOCK:
        to_check = check_fav(user_id, data)
        if not to_check:
            adder = Favourites(int(user_id), str(data))
            SESSION.add(adder)
            SESSION.commit()
            return True
        return False


def remove_fav(user_id):
    with FAV_INSERTION_LOCK:
        to_check = get_fav(user_id)
        if not to_check:
            return False
        rem = SESSION.query(Favourites).filter(Favourites.user_id == user_id)
        rem.delete()
        SESSION.commit()
        return True


def fav_count():
    try:
        return SESSION.query(Favourites).count()
    finally:
        SESSION.close()

