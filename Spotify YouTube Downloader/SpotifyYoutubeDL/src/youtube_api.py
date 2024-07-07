import sys
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Add the parent directory to the system path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from config.config import YOUTUBE_API_KEYS

api_key_index = 0

def search_youtube(song, artist):
    global api_key_index
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEYS[api_key_index])
    request = youtube.search().list(q=f"{song} {artist}", part='snippet', type='video', maxResults=1)
    try:
        response = request.execute()
        return response['items'][0]['id']['videoId'] if response['items'] else None
    except HttpError as e:
        if e.resp.status == 403 and 'quotaExceeded' in e.content.decode():
            api_key_index = (api_key_index + 1) % len(YOUTUBE_API_KEYS)
            print(f"Quota exceeded for API key. Switching to key {api_key_index + 1}")
            return search_youtube(song, artist)
        else:
            raise e
