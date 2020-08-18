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


from telegram import InlineKeyboardButton


def keyboard(
    ytkey=None,
    homepage=None,
    title=None,
    imdbid=None,
    tv_id=None,
    mv_id=None,
    anime_ytkey=None,
    anime_id=None,
    manga_id=None,
):
    """
    Attach InlineKeyboardButton dynamically from data
    """

    keyblist = [[]]
    if ytkey:
        if len(ytkey["results"]) > 0:
            ytkey = ytkey["results"][0]["key"]
            keyblist[0].append(
                InlineKeyboardButton(
                    text="📹 Trailer", url=f"https://www.youtube.com/watch?v={ytkey}"
                )
            )

    if homepage and homepage != "":
        keyblist.append([InlineKeyboardButton(text="📃 Homepage", url=homepage)])

    if imdbid:
        keyblist[0].append(
            InlineKeyboardButton(
                text="🎞️ IMDb", url=f"https://m.imdb.com/title/{imdbid}"
            )
        )

    if title:
        keyblist.append(
            [
                InlineKeyboardButton(
                    text="Save to watchlist 🔖", callback_data=f"addfav_{title[:54]}"
                )
            ]
        )

    if tv_id:
        keyblist.append(
            [
                InlineKeyboardButton(
                    text="More information",
                    url=f"https://www.themoviedb.org/tv/{tv_id}",
                )
            ]
        )

    if mv_id:
        keyblist.append(
            [
                InlineKeyboardButton(
                    text="More information",
                    url=f"https://www.themoviedb.org/movie/{mv_id}",
                )
            ]
        )

    if anime_ytkey:
        keyblist[0].append(
            InlineKeyboardButton(
                text="📹 Trailer", url=f"https://www.youtube.com/watch?v={anime_ytkey}"
            )
        )

    if anime_id:
        keyblist[0].append(
            InlineKeyboardButton(
                text="Information", url=f"https://kitsu.io/anime/{anime_id}"
            )
        )

    if manga_id:
        keyblist[0].append(
            InlineKeyboardButton(
                text="More Information", url=f"https://kitsu.io/manga/{manga_id}"
            )
        )
    return keyblist
