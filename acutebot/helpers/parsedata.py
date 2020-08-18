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


import itertools
from uuid import uuid4
from telegram.constants import MAX_CAPTION_LENGTH as MAX_CAP_LEN
from telegram import InlineQueryResultArticle, InputTextMessageContent


def byname(val):
    if val == "":
        return "Not available"
    datalist = []
    for x in val:
        datalist.append(x["name"])
    data = ", ".join(datalist)
    return data


def currency(val):
    """Format currency"""
    if val == "":
        return "Not available"
    curr = "${:,.2f}".format(val)
    return curr


def byindex(val):
    try:
        return val[0]["name"]
    except IndexError:
        return "Not Available"


def tvruntime(val):
    try:
        return str(val[0]) + " minutes"
    except IndexError:
        return "Not Available"


def article(
    title="", description="", message_text="", thumb_url=None, reply_markup=None
):
    return InlineQueryResultArticle(
        id=uuid4(),
        title=title,
        description=description,
        thumb_url=thumb_url,
        input_message_content=InputTextMessageContent(
            message_text=message_text, disable_web_page_preview=False
        ),
        reply_markup=reply_markup,
    )


def paginate(iterable, page_size):
    while True:
        i1, i2 = itertools.tee(iterable)
        iterable, page = (
            itertools.islice(i1, page_size, None),
            list(itertools.islice(i2, page_size)),
        )
        if len(page) == 0:
            break
        yield list(page)


def sort_caps(text, c_id, tv=False, mv=False, anime=False, manga=False):
    if len(text) > MAX_CAP_LEN:
        text = text[: MAX_CAP_LEN - 80]
        text += "</em>"
        if tv:
            text += f"<a href='https://www.themoviedb.org/tv/{c_id}'>...read more</a>"
        if mv:
            text += (
                f"<a href='https://www.themoviedb.org/movie/{c_id}'>...read more</a>"
            )
        if anime:
            text += f"<a href='https://kitsu.io/anime/{c_id}'>...read more</a>"
        if manga:
            text += f"<a href='https://kitsu.io/manga/{c_id}'>...read more</a>"

    return text
