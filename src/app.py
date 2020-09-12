import sys
import argparse

from gmusic     import GMusic
from spotify    import Spotify
from migrator   import GMusicToSpotifyMigrator


# functions
def process_options(options):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-sid', '--spotify-user-id',                                          help='Spotify user ID')
    parser.add_argument('-o',   '--output',         choices=['text', 'json'], default='text', help='Output format')

    options = parser.parse_args(options)

    return options


def main(options):
    options = process_options(options)

    gmusic  = GMusic()
    spotify = Spotify(options.spotify_user_id)

    migrator = GMusicToSpotifyMigrator(gmusic, spotify)

    migrator.migrate()

    if options.output == 'text':
        not_found_tracks_count = len(migrator.tracks_not_found)
        print(f'not found {not_found_tracks_count} tracks:')
        print('\n\n')

        for not_found_track in migrator.tracks_not_found:
            print(not_found_track.get('track'))
            print(not_found_track.get('gmusic_link'))
            print(not_found_track.get('search_link'))

        print('\n\n')
        print('\n\n')
        print('\n\n')

        not_filtered_tracks_count = len(migrator.tracks_not_filtered)
        print(f'not filtered {not_filtered_tracks_count} tracks:')
        print('\n\n')

        for not_filtered_track in migrator.tracks_not_filtered:
            print(not_filtered_track.get('track'))

            for found_track_version in not_filtered_track.get('founds'):
                print(found_track_version)

        print('\n\n')
        print('\n\n')
        print('\n\n')

        migrated_tracks_count = len(migrator.tracks_found)
        print(f'migrated {migrated_tracks_count} tracks:')
        print('\n\n')

        for migrated_track in migrator.tracks_found:
            print(migrated_track.get('track'))
            print(migrated_track.get('gmusic_link'))
            print(migrated_track.get('spotify_link'))

    else:
        output = {
            'migrated_tracks':      migrator.tracks_found,
            'not_found_tracks':     migrator.tracks_not_found,
            'not_filtered_tracks':  migrator.tracks_not_filtered
        }

        print(output)

if __name__ == '__main__':
    # first argument is script name, so we pass all arguments except of scipt name
    sys.exit(main(sys.argv[1:]))