import json
import requests
import youtube_dl
import os

YOUTUBE_VIDEO_URL = 'https://www.youtube.com/watch?v='
GOOGLE_API_URL = 'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={}&maxResults=3&order=date&type=video&key={}'
API_KEY = ''

CHANNEL_LIST = json.load(open('channels.json', 'r'))

__here__ = os.getcwd() + '\\'

def download_video(url, folder):
    ydl_options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '128',
        }],
        'outtmpl': __here__ + folder + '\%(title)s.%(ext)s',
        'prefer_ffmpeg': True,
        'download_archive': 'downloadedsongs.txt'
    }
    with youtube_dl.YoutubeDL(ydl_options) as ydl:
        ydl.extract_info(YOUTUBE_VIDEO_URL+url, download=True)


for channel in CHANNEL_LIST.values():
    r = requests.get(GOOGLE_API_URL.format(channel[0]['url'], API_KEY))
    recentsongs = json.loads(r.text)['items']
    for songs in recentsongs:
        download_video(songs['id']['videoId'], channel[0]['folder'])