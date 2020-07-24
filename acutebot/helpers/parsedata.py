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



from telegram.constants import MAX_CAPTION_LENGTH as MAX_CAP_LEN
from telegram.constants import MAX_MESSAGE_LENGTH as MAX_MSG_LEN

def byname(val):
    if val == "":
        return "Not available"
    datalist = list()
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

# Cut down text to fit in tg limited chars.
def sort_caps(text):
    if len(text) > MAX_CAP_LEN:
       text = text[:MAX_CAP_LEN - 5] + "</em>"
    return text

def sort_text(text):
    if len (text) > MAX_MSG_LEN:
       text = text[:MAX_MSG_LEN -9] + "</em>"
    return text
