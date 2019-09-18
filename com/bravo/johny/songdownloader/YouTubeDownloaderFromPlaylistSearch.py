import sys
import os
import youtube_dl
from googleapiclient.discovery import build
import json

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


def createDir(directory):
    if not os.path.exists(directory):
        os.mkdir(directory, 0o755)
    os.chdir(directory)


def getYouTubePlaylists():
    youtube = build('youtube', 'v3', developerKey=GOOGLE_API_KEY)

    req = youtube.search().list(q=PLAYLIST_SEARCH, part='snippet', type='playlist', maxResults=NO_OF_PLAYLIST_TO_DISPLAY)
    result = req.execute()

    r_json_str = json.dumps(result)
    r_json = json.loads(r_json_str)
    items = r_json.get('items')
    for item in items:
        playlistId = item.get('id').get('playlistId')
        title = item.get('snippet').get('title')
        playListIds.append(playlistId)
        playListTitles.append(title)


def getAllSongsFromAllPlayLists():
    youtube = build('youtube', 'v3', developerKey=GOOGLE_API_KEY)
    for playListId in playListIds:
        req = youtube.playlistItems().list(playlistId=playListId, part='snippet', maxResults=300)
        result = req.execute()
        r_json_str = json.dumps(result)
        r_json = json.loads(r_json_str)
        items = r_json.get('items')
        songTitles = []
        videoIds = []
        for item in items:
            title = item.get('snippet').get('title')
            if title == 'Private video':
                continue
            videoId = item.get('snippet').get('resourceId').get("videoId")
            songTitles.append(title)
            videoIds.append(videoId)

        songTitlesOfAllPlaylists.append(songTitles)
        videoIdsOfAllPlaylists.append(videoIds)


def displayPlaylistWithItsSongs():
    i = 0
    print("---------------------------------------------------------------------------------------\n")
    while i < NO_OF_PLAYLIST_TO_DISPLAY:
        print("Playlist number : " + str(i + 1) + "\n")
        print("Playlist title : " + playListTitles[i] + "\n")
        print("Songs in the playlist : " + str(songTitlesOfAllPlaylists[i]) + "\n")
        print("---------------------------------------------------------------------------------------\n")
        i = i+1


def prepareYouTubeSongUrls(videoIds):
    for videoId in videoIds:
        song_youtube_url_list.append(YOUTUBE_BASE_URL + videoId)


def downloadSongsFromYoutube():
    with youtube_dl.YoutubeDL(download_options) as dl:
        for song_url in song_youtube_url_list:
            dl.download([song_url])


def displaySongsInAPlaylist(songList):
    i = 1
    print("The playlist you selected has the following songs -- \n")
    for song in songList:
        print(str(i)+". "+song+"\n")
        i = i + 1


PLAYLIST_SEARCH = sys.argv[1]
DIRECTORY = '/tmp/YouTubeDownloads'
YOUTUBE_BASE_URL = "https://www.youtube.com/watch?v="
GOOGLE_API_KEY = "AIzaSyApLwmFqEBOS_bxj1DJRv_ULwWO-PKWQLY"
NO_OF_PLAYLIST_TO_DISPLAY = 6

song_youtube_url_list = []
playListIds = []
playListTitles = []
songTitlesOfAllPlaylists = []
videoIdsOfAllPlaylists = []

createDir(DIRECTORY)
getYouTubePlaylists()
getAllSongsFromAllPlayLists()
displayPlaylistWithItsSongs()
user_input = input('Which playlist should we download for you : ')
displaySongsInAPlaylist(songTitlesOfAllPlaylists[int(user_input)-1])
prepareYouTubeSongUrls(videoIdsOfAllPlaylists[int(user_input)-1])
downloadSongsFromYoutube()
