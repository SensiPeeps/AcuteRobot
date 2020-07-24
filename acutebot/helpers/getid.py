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



import requests as r
from acutebot import TMDBAPI

base_url = "https://api.themoviedb.org/3"

def getid(query, type=None):
    """
    Returns TV or movie id for the query
    """

    query = query.replace(" ", "%20")
    id = 0

    if type and type == "TV":

        id = r.get(
            f"{base_url}/search/tv?api_key={TMDBAPI}"
            + f"&language=en&query={query}"
            + "&page=1&include_adult=true"
        )

    if type and type == "MOVIE":

        id = r.get(
            f"{base_url}/search/movie?api_key={TMDBAPI}"
            + f"&language=en&query={query}"
            + "&page=1&include_adult=true"
        )

    if id.status_code != 200:
        return "api_error"

    try:
        id = id.json()["results"][0]["id"]
    except IndexError:
        return "not_found"

    return id
