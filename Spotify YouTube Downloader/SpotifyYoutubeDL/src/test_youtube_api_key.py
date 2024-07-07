from googleapiclient.discovery import build

YOUTUBE_API_KEY = 'AIzaSyC9czWrQRKexKnL7nzXaOzc2MoAGxdAItU'

def test_youtube_api():
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    request = youtube.search().list(q="test", part='snippet', type='video', maxResults=1)
    response = request.execute()
    print(response)

if __name__ == "__main__":
    test_youtube_api()
