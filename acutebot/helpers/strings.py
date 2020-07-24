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



# Contents
MOVIE_STR = """
️<b>{}</b> : {}

• Status : <pre>{}</pre>
• Genres : <pre>{}</pre>
• Languages : <pre>{}</pre>
• Runtime : <pre>{} minutes</pre>
• Budget : <pre>{}</pre>
• Revenue : <pre>{}</pre>
• Release Date : <pre>{}</pre>
• Average Rating : <pre>{}</pre>
• Popularity : <pre>{}</pre>

• OverView : <em>{}</em>
"""

TV_STR = """
<b>{}</b>

• Created by : <pre>{}</pre>
• Genres : <pre>{}</pre>
• Languages : <pre>{}</pre>
• Episodes Runtime : <pre>{}</pre>
• First aired : <pre>{}</pre>
• Last aired : <pre>{}</pre>
• Status : <pre>{}</pre>
• Seasons : <pre>{}</pre>
• Total EPs : <pre>{}</pre>
• Average Rating : <pre>{}</pre>
• Production Company : <pre>{}</pre>

• OverView : <em>{}</em>
"""

# Start
START_STRING = """
Hey there, my name is Acute & you can ask me \
about details of any movies or TV shows, i can \
also save them into your watchlist & much more! \
click: [<pre>/</pre>] in your keyboard to see list of possible commands. \
and don't forget to smile, atleast once in a while :)
"""
START_STRING_GRP = "Hmmm?"


# Errors
API_ERR = "Sorry, couldn't reach API at the moment :("
NOT_FOUND = "Sorry, couldn't find any results for the query :("
REVIEW_NOT_FOUND = "Sorry, It looks like i don't have reviews for that title in my database :("
INVALIDREVIEWNAME = "Hmmm.. maybe you've sent wrong category to look for, please try again!"

# Cancel
CANCEL = "Cancelled the current task!"

# To search
TOSEARCHMOVIE = "Please reply with the movie title you wanna look for!"
TOSEARCHTV = "Please reply with the TV title you wanna look for!"
TOSEARCHREVIEW = "Hi! Please tell me for what category you want reviews for."

# Favs
NOFAVS = "Hmmm 🤔 looks like you don't have any title saved in your watchlist yet!"
REMFAV = "Successfully cleared your watchlist."
SAVED_FAV = "Added {} to your Watchlist!"
FAV_EXIST = "Hey there this title is already in your watchlist, Go & finish it instead ;)"


#Stats
STATS = """
📊 Current Stats;
👥 Total users : {}
💛 Watchlist saved : {}
"""

#Greet
GREET = "Hey {}! Thank you for adding me in {} :)"

# Lyrics
SONGNAME = "Please tell me name of the song you want lyrics for."
ARTISTNAME = "Great! now tell me name of the artist for this song."

LYRICS_ERR = """Sorry, looks like i forgot your song name, possibly due to restart \
Would you mind sending me again?
"""
LYRIC_NOT_FOUND = "Sorry i couldn't find lyrics for that song."
LYRICS_TOO_BIG = "Lyrics of this song is too big for telegram, I'm sending it as a file..."

# Music
MUSICQ = "Please choose the quality of music :)"
MUSICNAME = "Okay! tell me name of the song you're looking for."
MUSICNOTFOUND = "Sorry i couldn't find that song :("
