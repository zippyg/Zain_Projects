import sys
import os

# Add the parent directory to the system path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from googleapiclient.discovery import build
from config.config import YOUTUBE_API_KEY

def test_youtube_api():
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    request = youtube.search().list(q="test", part='snippet', type='video', maxResults=1)
    response = request.execute()
    print(response)

if __name__ == "__main__":
    test_youtube_api()
