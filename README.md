# Migrate from Google Play Music to Spotify

Script that migrates liked songs from Google Play Music to Spotify


## requirements

- python 3.8+


## how to use

- install pipenv
```
py -m pip install pipenv
```
- install dependencies
```
py -m pipenv install
```
- register Spotify app - https://developer.spotify.com/documentation/general/guides/app-settings/
  - specify redirect URI to `http://localhost`
- go to https://www.spotify.com/ua/account/overview/ and copy `Username`
- set environment with credentials
```
SET SPOTIPY_CLIENT_ID=client_id_here
SET SPOTIPY_CLIENT_SECRET=client_secret_here
SET SPOTIPY_REDIRECT_URI=http://localhost
```
- configure python to use UTF-8 for output
```
SET PYTHONIOENCODING=utf-8
```
- run migration
```
py -m pipenv run py .\src\app.py --spotify-user-id SPOTIFY_USER_ID
```
- follow prompts to allow access to Google Music and Spotify


## dependencies

- [gmusicapi: an unofficial API for Google Play Music](https://github.com/simon-weber/gmusicapi)
- [Spotipy: A light weight Python library for the Spotify Web API](https://github.com/plamere/spotipy)