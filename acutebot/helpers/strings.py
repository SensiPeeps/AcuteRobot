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


from acutebot import __version__
from platform import python_version
from telegram import __version__ as _libv_

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

ANIME_STR = """
<b>{}</b> | <b>{}</b>

• Category : <pre>{}</pre>
• Type : <pre>{}</pre>
• Average Rating : <pre>{}</pre>
• Status : <pre>{}</pre>
• First aired : <pre>{}</pre>
• Last aired : <pre>{}</pre>
• Runtime : <pre>{} minutes</pre>
• No of episodes : <pre>{}</pre>

• Synopsis : <em>{}</em>
"""

# Inline Content
INLINE_STR = """
• <b>Title</b> : {}
• <b>Release</b> : <pre>{}</pre>
• <b>Popularity</b> : <pre>{}</pre>
• <b>Language</b> : <pre>{}</pre>
• <b>Average Rating</b> : <pre>{}</pre>

• <b>OverView</b> : <em>{}</em>
"""

INLINE_DESC = """
<b>Usage:</b> <pre>&lt;tv&gt; title</pre> <b>or</b> <pre>&lt;movie&gt; title</pre> <b>in inline query.</b>

Examples:
× <pre>&lt;movie&gt; Avengers Endgame</pre>
× <pre>&lt;tv&gt; Breaking Bad</pre>
× <pre>&lt;anime&gt; Attack on Titan</pre>
• You can try on buttons below!
"""


# Start
START_STRING = """
Hey {}, my name is acutebot and i can help you to get \
information about your favorite movies, tv and anime shows, you can also download \
music & can view song lyrics using me! Just click the button \
below to get started with list of possible commands...

And don't forget to smile, atleast once in a while ;)
"""
START_STRING_GRP = "Hmmm?"


# About
ABOUT_STR = f"""
I'm fully written in \
Python3 by <a href="tg://user?id=894380120">starry</a>, \
feel free to report him if you find any rough edge inside me.

× Bot version : <pre>{__version__}</pre>
× Python version : <pre>{python_version()}</pre>
× Library version : <pre>PTB {_libv_}</pre>
× Movies & TV data : <pre>themoviedb.org</pre>
× Anime data from : <pre>kitsu.io</pre>
× Music data from : <pre>deezer.com</pre>
× Lyrics data from : <pre>genius.com</pre>

If you enjoyed using me & wanna support my creator \
hit the donate button below, since he's just a student so \
every little helps to pay for my server, and ofcourse boosting morale ;)

"""

# Help
HELP_STR = """
<b>🗒️ Documentation for possible commands :</b>

❄️ <b>Movies, TV & Anime commands :</b>
✓ /movies : Get information about movies.
✓ /tvshows : Get information about tvshows.
✓ /anime : Get information about your favorite anime.

❄️ <b>Music & lyrics related commands :</b>
√ /music : Download your favorite songs in high resolution
√ /lyrics : Get lyrics for your favorite songs.

❄️ <b>Miscellaneous commands :</b>
√ /reddit : Gets you random memes scraped from popular subreddits.
√ /watchlist : Get list of saved shows from your watchlist :D.
√ /cancel : Do this when you get stuck & bot is not replying to you.

🏷 Notes: You can also search movies, tvshows & anime inline! \
just type <pre>@acutebot</pre> in your message box \
and follow the instructions.

"""


# Errors
API_ERR = "Sorry, couldn't reach API at the moment :("
NOT_FOUND = "Sorry, couldn't find any results for the query :("
INVALIDCAT = "Hmmm.. maybe you've sent wrong category to look for, please try again!"

# Cancel
CANCEL = "Cancelled the current task!"

# To search
TOSEARCHMOVIE = "Please reply with the movie title you wanna look for."
TOSEARCHTV = "Please reply with the TV title you wanna look for."
TOSEARCH_ANIME = "Please reply with the anime title you want to look for."

# Favs
NOFAVS = "Hmmm 🤔 looks like you don't have any title saved in your watchlist yet!"
REMFAV = "Great work! Successfully cleared your watchlist :)"
SAVED_FAV = "Added '{}' to your Watchlist!"
FAV_EXIST = (
    "Hey there this title is already in your watchlist, Go & finish it instead ;)"
)
NOT_ALLOWED = "You're not allowed to do this!"

# Stats
STATS = """
📊 Current Stats;
👥 Total users : {}
💛 Watchlist saved : {}
"""

# Greet
GREET = "Hey {}! Thank you for adding me in {} :)"

# Lyrics
SONGNAME = "Please tell me name of the song you want lyrics for."
ARTISTNAME = "Great! now tell me name of the artist for this song."

LYRICS_ERR = """Sorry, looks like i forgot your song name, possibly due to restart \
Would you mind sending me again?
"""
LYRIC_NOT_FOUND = "Sorry i couldn't find lyrics for that song."
LYRICS_TOO_BIG = (
    "Lyrics of this song is too big for telegram, I'm sending it as a file..."
)

# Music
MUSICQ = "Please choose the quality of music :)"
MUSICNAME = "Okay! tell me name of the song you're looking for."
UPLOAD_BOTAPI = "⌛ uploading song please wait..."
UPLOAD_MTPROTO = "Hmm, file size is more than 50MBs, uploading via mtproto this might take around 5 mins, please wait..."
MUSICNOTFOUND = "Sorry i couldn't find that song :("

# Lookup
WRONG_FILE = "Sorry but i can only lookup for images, sticker and gifs!"
BAD_FILE = "No sauce found; invalid file size..."
L_LIMIT = "Looks like i've reached my API limits, please try later!"
S_LIMIT = "Short limit reached please try after few minutes!"
LOOKUP_NOREPLY = "Please reply to some photo, gif, or sticker to lookup!"
