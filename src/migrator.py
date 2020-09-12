class GMusicToSpotifyMigrator:
    def __init__(self, gmusic, spotify):
        self.__gmusic     = gmusic
        self.__spotify    = spotify

        self.tracks_not_found    = []
        self.tracks_not_filtered = []
        self.tracks_found        = []

    def __filter_by_album(self, tracks, album_name):
        filtered_tracks = []

        for track in tracks:
            track_album_name = track.get('album').get('name')

            if track_album_name == album_name:
                filtered_tracks.append(track)

        return filtered_tracks

    def __filter_by_popularity(self, tracks):
        most_popular_track = tracks[0]

        for track in tracks:
            track_popularity = track.get('popularity')

            if most_popular_track.get('popularity') < track_popularity:
                most_popular_track = track

        return most_popular_track

    def __filter_tracks(self, tracks, filter_data):
        filtered_track = None

        filters = [
            {
                'function':   self.__filter_by_album,
                'filter_by':  'album'
            }

            # todo: filter by title
        ]

        for filter in filters:
            filter_function = filter.get('function')
            filter_by       = filter.get('filter_by')

            filter_value    = filter_data.get(filter_by)

            filtered_tracks_list = filter_function(tracks, filter_value)

            if len(filtered_tracks_list) == 1:
                filtered_track = filtered_tracks_list[0]
                break

            if len(filtered_tracks_list) == 0:
                break

        if filtered_track == None and len(filtered_tracks_list) > 0:
            filtered_track = self.__filter_by_popularity(filtered_tracks_list)

        return filtered_track

    def migrate(self):
        gmusic_liked_tracks = self.__gmusic.get_liked_tracks()
        spotify_tracks_ids  = []

        for track in gmusic_liked_tracks:
            title       = track.get('title')
            artist      = track.get('artist')
            year        = track.get('year')
            album       = track.get('album')
            album_id    = track.get('albumId')
            track_id    = track.get('id')
            track_nid   = track.get('nid')

            search_track_in_spotify_result = self.__spotify.search_track_in_spotify(title, artist, album, year)

            found_tracks        = search_track_in_spotify_result.get('tracks')
            found_tracks_count  = found_tracks.get('total')

            if found_tracks_count == 0:
                self.tracks_not_found.append({
                    'track':        { 'title': title, 'artist': artist, 'album': album, 'year': year },
                    'gmusic_link':  f'https://play.google.com/music/m/T{track_nid}',
                    'search_link':  f'https://open.spotify.com/search/{title} artist:{artist} album:{album} year:{year}'
                })
                continue

            found_track = None
            if found_tracks_count > 1:
                found_tracks_list   = found_tracks.get('items')

                found_track = self.__filter_tracks(
                    found_tracks_list,
                    { 'title': title, 'artist': artist, 'album': album, 'year': year }
                )

                if found_track == None:
                    spotify_tracks_links                = list(map(lambda track: { 'popularity': track.get('popularity'), 'link': track.get('external_urls').get('spotify')}, found_tracks_list))
                    spotify_tracks_links_by_popularity  = newlist = sorted(spotify_tracks_links, key=lambda item: item.get('popularity'), reverse = True)
                    self.tracks_not_filtered.append({
                        'track': { 'title': title, 'artist': artist, 'album': album, 'year': year },
                        'gmusic_link':  f'https://play.google.com/music/m/T{track_nid}',
                        'founds': spotify_tracks_links_by_popularity
                    })
                    continue
            else:
                found_track = found_tracks.get('items')[0]


            self.tracks_found.append({
                'track':        { 'title': title, 'artist': artist, 'album': album, 'year': year },
                'gmusic_link':  f'https://play.google.com/music/m/T{track_nid}',
                'spotify_link': found_track.get('external_urls').get('spotify')
            })

            spotify_tracks_ids.append(found_track.get('id'))

        batch_size = 50
        for i in range(0, len(spotify_tracks_ids), batch_size):
            spotify_tracks_ids_batch = spotify_tracks_ids[i:i + batch_size]

            self.__spotify.add_tracks_to_liked(spotify_tracks_ids_batch)