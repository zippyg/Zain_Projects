# downloader.py
import os
import yt_dlp
import requests
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC, error

def download_song(video_id, song_name, artist_name, cover_art_url, output_dir='downloads'):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_dir, f"{song_name}.%(ext)s"),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f'http://www.youtube.com/watch?v={video_id}'])
    except yt_dlp.utils.DownloadError as e:
        print(f"Error downloading {song_name}: {e}")
        return False

    mp3_path = os.path.join(output_dir, f"{song_name}.mp3")

    # Download cover art directly into memory
    response = requests.get(cover_art_url)
    cover_art_data = response.content

    # Embed cover art into mp3
    try:
        audio = ID3(mp3_path)
    except error:
        audio = ID3()

    audio.add(APIC(
        encoding=3,  # 3 is for utf-8
        mime='image/jpeg',  # image/jpeg or image/png
        type=3,  # 3 is for the cover (front) image
        desc='Cover',
        data=cover_art_data
    ))

    audio.save(mp3_path)

    # Add song and artist metadata
    audio = EasyID3(mp3_path)
    audio['title'] = song_name
    audio['artist'] = artist_name
    audio.save()
    
    return True
