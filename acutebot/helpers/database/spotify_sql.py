import threading

from sqlalchemy import Column, Integer, UnicodeText
from acutebot.helpers.database import SESSION, BASE


class SpotifyCreds(BASE):
    __tablename__ = "spotifycreds"
    user_id = Column(Integer, primary_key=True)
    spotify_id = Column(UnicodeText)
    spotify_access_token = Column(UnicodeText)
    spotify_refresh_token = Column(UnicodeText)

    def __init__(
        self,
        user_id,
        spotify_id=None,
        spotify_access_token=None,
        spotify_refresh_token=None,
    ):
        self.user_id = user_id
        self.spotify_id = spotify_id
        self.spotify_access_token = spotify_access_token
        self.spotify_refresh_token = spotify_refresh_token


SpotifyCreds.__table__.create(checkfirst=True)
SPT_INSERTION_LOCK = threading.RLock()


def update_creds(
    user_id, spotify_id=None, spotify_access_token=None, spotify_refresh_token=None
):
    with SPT_INSERTION_LOCK:
        sptcreds = SESSION.query(SpotifyCreds).get(user_id)
        if not sptcreds:
            sptcreds = SpotifyCreds(
                user_id, spotify_id, spotify_access_token, spotify_refresh_token
            )
            SESSION.add(sptcreds)
            SESSION.flush()
        else:
            sptcreds.spotify_id = spotify_id
            sptcreds.spotify_access_token = spotify_access_token
            sptcreds.spotify_refresh_token = spotify_refresh_token
        SESSION.commit()


def get_sptuser(user_id):
    try:
        return (SESSION.query(SpotifyCreds).get(user_id)).__dict__
    finally:
        SESSION.close()
