# spotify_api.py
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

def get_spotify_client(client_id, client_secret, redirect_uri):
    sp_oauth = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
    token_info = sp_oauth.get_access_token()
    sp = Spotify(auth=token_info['access_token'])
    return sp

def get_liked_songs(sp):
    results = sp.current_user_saved_tracks()
    songs = []
    while results:
        for item in results['items']:
            track = item['track']
            song_name = track['name']
            artist_name = track['artists'][0]['name']
            cover_art_url = track['album']['images'][0]['url'] if track['album']['images'] else None
            songs.append((song_name, artist_name, cover_art_url))
        if results['next']:
            results = sp.next(results)
        else:
            results = None
    return songs

def get_playlist_songs(sp, playlist_id):
    results = sp.playlist_tracks(playlist_id)
    songs = []
    while results:
        for item in results['items']:
            track = item['track']
            song_name = track['name']
            artist_name = track['artists'][0]['name']
            cover_art_url = track['album']['images'][0]['url'] if track['album']['images'] else None
            songs.append((song_name, artist_name, cover_art_url))
        if results['next']:
            results = sp.next(results)
        else:
            results = None
    return songs


