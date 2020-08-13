from pyfy import Spotify as Pyfy, ClientCreds, UserCreds
from pyfy.excs import ApiError
from dataclasses import dataclass
from telegram import Bot

from acutebot import TOKEN, SPT_CLIENT_SECRET, SPT_CLIENT_ID, APP_URL
from acutebot.helpers.database.spotify_sql import update_creds, get_sptuser

import tornado.web
import typing

bot = Bot(TOKEN)


@dataclass
class Music:
    id: str
    name: str
    artist: str
    url: str
    thumbnail: str

    def __init__(self, music: dict):
        self.id = music["id"]
        self.name = music["name"]
        self.artist = music["artists"][0]["name"]
        self.url = music["external_urls"]["spotify"]
        self.thumbnail = music["album"]["images"][1]["url"]


class Spotify:
    def __init__(self, user: dict):

        self._client = SpotifyClient(
            access_token=user["spotify_access_token"],
            refresh_token=user["spotify_refresh_token"],
        )

    @property
    def current_music(self) -> typing.Optional[Music]:
        try:
            current_status = self._client.currently_playing()
            music = current_status["item"]
            return Music(music)
        except Exception:
            return

    @property
    def last_music(self) -> Music:
        music = self._client.recently_played_tracks(limit=1)["items"][0]["track"]
        return Music(music)


class SpotifyClient(Pyfy):
    def __init__(
        self, access_token=None, refresh_token=None,
    ):
        scopes = [
            "user-read-recently-played",
            "user-read-playback-state",
        ]

        user_creds = None

        if access_token and refresh_token:
            user_creds = UserCreds(
                access_token=access_token, refresh_token=refresh_token
            )

        super().__init__(
            client_creds=ClientCreds(
                client_id=SPT_CLIENT_ID,
                client_secret=SPT_CLIENT_SECRET,
                redirect_uri=APP_URL + "acutebot/webserver",
                scopes=scopes,
            ),
            user_creds=user_creds,
        )


def get_spotify_data(user_id):
    try:
        user = get_sptuser(user_id)
    except Exception:
        return False

    return Spotify(user)


# Tornado web handlers for login.


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("test")


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
