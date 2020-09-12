import spotipy
import spotipy.util as util


class Spotify:
    def __init__(self, username):
        # https://developer.spotify.com/documentation/general/guides/scopes/
        self._scope = "user-library-read user-library-modify"

        token = util.prompt_for_user_token(username, self._scope)
        self._client = spotipy.Spotify(auth=token)

    def __split_list_on_chunks(self, list, chank_size):
        for i in range(0, len(list), chank_size):
            yield list[i:i + chank_size]

    # get user liked tracks list
    def get_liked_tracks(self):
        liked_tracks = []

        offset  = 0
        limit   = 50
        while True:
            current_user_saved_tracks_response = self._client.current_user_saved_tracks(limit=50, offset=offset)

            liked_tracks.extend(current_user_saved_tracks_response.get('items'))

            if current_user_saved_tracks_response.get('next') == None:
                break

            offset = offset + limit

        return liked_tracks

    # cleanup user liked tracks list
    def cleanup_liked_tracks(self):
        liked_tracks = self.get_liked_tracks()

        liked_tracks_ids = list(map(lambda track: track.get('track').get('id'), liked_tracks))

        batch_size = 50
        chanked_liked_tracks_ids = self.__split_list_on_chunks(liked_tracks_ids, batch_size)

        for ids_batch in chanked_liked_tracks_ids:
            self._client.current_user_saved_tracks_delete(tracks = ids_batch)

    # return list of tracks found by specified params
    def search_track_in_spotify(self, title, artist, album, year):
        query = f'{title} artist:{artist} album:{album} year:{year}'

        search_results = self._client.search(q=query, type='track')

        return search_results

    def add_tracks_to_liked(self, tracks_ids):
        self._client.current_user_saved_tracks_add(tracks=tracks_ids)