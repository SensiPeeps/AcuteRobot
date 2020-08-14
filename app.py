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


import os, tornado
from telegram import Bot
from acutebot import TOKEN
from acutebot.helpers.database.spotify_sql import update_creds
from acutebot.helpers.spthelper import SpotifyClient


bot = Bot(TOKEN)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello World!")


class SpotifyCallback(tornado.web.RequestHandler):
    def get(self):
        if self.get_argument("code", ""):
            grant = self.get_argument("code", "")
            callback_state = self.get_argument("state", "")
            spotify = SpotifyClient()
            user_creds = spotify.build_user_creds(grant=grant)
            update_creds(
                callback_state,
                user_creds.id,
                user_creds.access_token,
                user_creds.refresh_token,
            )
            print("user logged in successfully")
            bot.sendMessage(callback_state, "Successfully logged in!")
            self.redirect("https://t.me/" + bot.username)


urls = [(r"/", MainHandler), (r"/acutebot/webserver", SpotifyCallback)]
PORT = os.environ.get("PORT", 8888)


def start():

    print("Tornado server started")

    app = tornado.web.Application(urls)
    app.listen(PORT, address="0.0.0.0")
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    start()
