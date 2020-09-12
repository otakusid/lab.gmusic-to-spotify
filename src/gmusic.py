import os

from gmusicapi import Mobileclient


class GMusic:
    def __init__(self):
        self._client = Mobileclient()

        # auth information stored in client.OAUTH_FILEPATH path by default
        is_user_authenticated = os.path.exists(self._client.OAUTH_FILEPATH)
        if is_user_authenticated == False:
            self.authenticate_in_google()

        is_logged_in = self._client.oauth_login(device_id = Mobileclient.FROM_MAC_ADDRESS)

        if is_logged_in == False:
            raise 'Login to Google Play Music failed'

    def authenticate_in_google():
        self._client.perform_oauth()

    def get_liked_tracks(self):
        liked_tracks = self._client.get_top_songs()

        return liked_tracks