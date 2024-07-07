import sys
import os
import time
from requests.exceptions import ReadTimeout

# Add the parent directory to the system path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from spotify_api import get_spotify_client, get_liked_songs, get_playlist_songs
from youtube_api import search_youtube
from downloader import download_song
from config.config import YOUTUBE_API_KEYS

def main():
    # Get user input for Spotify API credentials
    client_id = input("Enter your Spotify Client ID: ")
    client_secret = input("Enter your Spotify Client Secret: ")
    redirect_uri = input("Enter your Spotify Redirect URI: ")

    # Initialize Spotify client with user-provided credentials
    sp = get_spotify_client(client_id, client_secret, redirect_uri)

    # Get available playlists
    playlists = sp.current_user_playlists()
    print("\nAvailable Playlists:")
    print("0. Liked Songs")
    for idx, playlist in enumerate(playlists['items']):
        print(f"{idx + 1}. {playlist['name']}")

    # Prompt user to select a playlist
    playlist_idx = int(input("\nEnter the number of the playlist you want to download: "))
    if playlist_idx == 0:
        playlist_name = "Liked Songs"
        playlist_songs = get_liked_songs(sp)
    else:
        playlist_id = playlists['items'][playlist_idx - 1]['id']
        playlist_name = playlists['items'][playlist_idx - 1]['name']
        retries = 5
        for attempt in range(retries):
            try:
                # Get songs from the selected playlist
                playlist_songs = get_playlist_songs(sp, playlist_id)
                break
            except ReadTimeout:
                if attempt < retries - 1:
                    print(f"ReadTimeout occurred. Retrying ({attempt + 1}/{retries})...")
                    time.sleep(5)  # Wait before retrying
                else:
                    print("Failed to retrieve playlist songs after several attempts.")
                    return

    print(f"\nYou selected: {playlist_name}")

    # Get user input for download path and validate it
    while True:
        custom_download_dir = input("Enter the path where you want to save the music: ")
        if custom_download_dir:
            if not os.path.exists(custom_download_dir):
                os.makedirs(custom_download_dir)
            break
        else:
            print("Please enter a valid path.")

    # Download each song
    for song, artist in playlist_songs:
        print(f"Searching for {song} by {artist}")
        video_id = search_youtube(song, artist)
        if video_id:
            print(f"Downloading {song}")
            download_song(video_id, output_dir=custom_download_dir)
        else:
            print(f"Could not find {song} by {artist} on YouTube")

if __name__ == "__main__":
    main()
