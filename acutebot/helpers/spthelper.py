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


from pyfy import Spotify as Pyfy, ClientCreds, UserCreds
from pyfy.excs import ApiError
from dataclasses import dataclass

from acutebot import TOKEN, SPT_CLIENT_SECRET, SPT_CLIENT_ID, APP_URL
from acutebot.helpers.database.spotify_sql import get_sptuser

import typing


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
    def __init__(self, user):

        try:
            self._client = SpotifyClient(
                access_token=user.spotify_access_token,
                refresh_token=user.spotify_refresh_token,
            )
        except ApiError:
            raise Exception("tokens invalid")

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
        return Spotify(user)
    except Exception:
        return False
