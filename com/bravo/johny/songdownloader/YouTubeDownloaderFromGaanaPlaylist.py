from bs4 import BeautifulSoup as soup
import urllib.request
from googleapiclient.discovery import build
from re import search
import os
import ssl
import re
import json
import youtube_dl

download_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(title)s.%(ext)s',
    'nocheckcertificate': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}


def disableSSL():
    if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
            getattr(ssl, '_create_unverified_context', None)):
        ssl._create_default_https_context = ssl._create_unverified_context


def createDir(directory):
    if not os.path.exists(directory):
        os.mkdir(directory, 0o755)
    os.chdir(directory)


def getSongsFromAGaanaPlaylistInAList(playlist_url):
    uClient = urllib.request.urlopen(playlist_url)
    page_html = uClient.read()
    uClient.close()

    page_soup = soup(page_html, "html.parser")

    song_rows = page_soup.select('ul[class*="s_l artworkload"]')
    for song_row in song_rows:
        song_title_link = song_row.select('li[class*="s_title"]')[0]
        song = song_title_link.find("a", {"class": "sng_c"})
        song_name_list.append(song.text)


def getSongURLSInAList():
    youtube = build('youtube', 'v3', developerKey=GOOGLE_API_KEY)

    for song in song_name_list:
        req = youtube.search().list(q=song, part='snippet', type='video', maxResults=5)
        result = req.execute()

        r_json_str = json.dumps(result)
        r_json = json.loads(r_json_str)
        items = r_json.get('items')
        for item in items:
            videoId = item.get('id').get('videoId')
            title = item.get('snippet').get('title')
            description = item.get('snippet').get('description')

            found_match_in_title = search(MATCHING_STRING, title, re.IGNORECASE)
            found_match_in_description = search(MATCHING_STRING, description, re.IGNORECASE)

            if found_match_in_title:
                song_youtube_url_list.append(YOUTUBE_BASE_URL + videoId)
                print("Following song will be downloaded : "+title)
                break


def downloadSongsFromYoutube():
    with youtube_dl.YoutubeDL(download_options) as dl:
        for song_url in song_youtube_url_list:
            dl.download([song_url])


GAANA_PLAYLIST_URL = "https://gaana.com/artist/shyamal-mitra"
MATCHING_STRING = "Shyamal Mitra"
DIRECTORY = '/tmp/Gaana'
YOUTUBE_BASE_URL = "https://www.youtube.com/watch?v="
GOOGLE_API_KEY = "AIzaSyApLwmFqEBOS_bxj1DJRv_ULwWO-PKWQLY"

song_name_list = []
song_youtube_url_list = []

disableSSL()
createDir(DIRECTORY)
getSongsFromAGaanaPlaylistInAList(GAANA_PLAYLIST_URL)
getSongURLSInAList()
downloadSongsFromYoutube()

print(len(song_name_list))
print(str(len(song_youtube_url_list))+" songs have been downloaded !!")