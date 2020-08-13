import os, tornado
from telegram import Bot
from acutebot import TOKEN
from acutebot.helpers.database.spotify_sql import update_creds


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
    app.listen(PORT, address='0.0.0.0')
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
   start()
