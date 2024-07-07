from downloader import download_song

def test_download():
    video_id = 'dQw4w9WgXcQ'  # Example video ID (Rick Astley - Never Gonna Give You Up)
    download_song(video_id)

if __name__ == "__main__":
    test_download()
