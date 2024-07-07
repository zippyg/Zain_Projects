import os

# Define directory and file structure
project_structure = {
    "SpotifyYoutubeDL": {
        "src": {
            "main.py": """from spotify_api import get_spotify_client, get_liked_songs, get_playlist_songs
from youtube_api import search_youtube
from downloader import download_song

def main():
    sp = get_spotify_client()

    # Get liked songs
    liked_songs = get_liked_songs(sp)

    # Or get songs from a specific playlist
    # playlist_id = 'your_playlist_id'
    # playlist_songs = get_playlist_songs(sp, playlist_id)

    for song, artist in liked_songs:
        print(f"Searching for {song} by {artist}")
        video_id = search_youtube(song, artist)
        if video_id:
            print(f"Downloading {song}")
            download_song(video_id)
        else:
            print(f"Could not find {song} by {artist} on YouTube")

if __name__ == "__main__":
    main()
            """,
            "spotify_api.py": """import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config.config import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI

def get_spotify_client():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                                   client_secret=SPOTIPY_CLIENT_SECRET,
                                                   redirect_uri=SPOTIPY_REDIRECT_URI,
                                                   scope="user-library-read playlist-read-private"))
    return sp

def get_liked_songs(sp):
    results = sp.current_user_saved_tracks()
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return [(item['track']['name'], item['track']['artists'][0]['name']) for item in tracks]

def get_playlist_songs(sp, playlist_id):
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return [(item['track']['name'], item['track']['artists'][0]['name']) for item in tracks]
            """,
            "youtube_api.py": """from googleapiclient.discovery import build
from config.config import YOUTUBE_API_KEY

def search_youtube(song, artist):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    request = youtube.search().list(q=f"{song} {artist}", part='snippet', type='video', maxResults=1)
    response = request.execute()
    return response['items'][0]['id']['videoId'] if response['items'] else None
            """,
            "downloader.py": """import os
import yt_dlp

def download_song(video_id, output_dir='downloads'):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f'http://www.youtube.com/watch?v={video_id}'])
            """,
        },
        "config": {
            "config.py": """SPOTIPY_CLIENT_ID = 'your_spotify_client_id'
SPOTIPY_CLIENT_SECRET = 'your_spotify_client_secret'
SPOTIPY_REDIRECT_URI = 'your_spotify_redirect_uri'
YOUTUBE_API_KEY = 'your_youtube_api_key'
            """,
        },
        "requirements.txt": """spotipy
pytube
yt-dlp
google-api-python-client
            """,
        "README.md": """# Spotify to YouTube Downloader

This project allows you to download your liked songs or songs from a playlist on Spotify from YouTube.

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/your_username/SpotifyYoutubeDL.git
    cd SpotifyYoutubeDL
    ```

2. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Configure your API keys in `config/config.py`.

4. Run the script:
    ```sh
    python src/main.py
    ```

## Usage

- The script fetches your liked songs from Spotify and downloads them from YouTube.
- You can also modify the script to download songs from a specific playlist.

## Dependencies

- spotipy
- pytube
- yt-dlp
- google-api-python-client

## License

This project is licensed under the MIT License.
            """
    }
}

# Function to create directories and files
def create_project_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_project_structure(path, content)
        else:
            with open(path, 'w') as file:
                file.write(content)

# Create the project structure
base_path = os.getcwd()
create_project_structure(base_path, project_structure)

print("Project structure created successfully!")
