import concurrent.futures
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
        resultCount = 0
        songTitles = []
        videoIds = []
        req = youtube.playlistItems().list(playlistId=playListId, part='snippet', maxResults=50)
        while True:
            result = req.execute()
            r_json_str = json.dumps(result)
            r_json = json.loads(r_json_str)
            items = r_json.get('items')
            nextPageToken = r_json.get('nextPageToken')
            for item in items:
                title = item.get('snippet').get('title')
                if title == 'Private video':
                    continue
                videoId = item.get('snippet').get('resourceId').get("videoId")
                songTitles.append(title)
                videoIds.append(videoId)

            resultCount = resultCount + 50
            if nextPageToken is None or resultCount > MAXIMUM_NUMBER_OF_SONGS_TO_DOWNLOAD:
                break
            req = youtube.playlistItems().list(playlistId=playListId, part='snippet', maxResults=50, pageToken=nextPageToken)

        songTitlesOfAllPlaylists.append(songTitles)
        videoIdsOfAllPlaylists.append(videoIds)


def displayPlaylistWithItsSongs():
    i = 0
    print("---------------------------------------------------------------------------------------\n")
    while i < NO_OF_PLAYLIST_TO_DISPLAY:
        print("Playlist number : " + str(i + 1) + "\n")
        print("Playlist title : " + playListTitles[i] + "\n")
        print("Number of songs in the playlist : " + str(len(songTitlesOfAllPlaylists[i])))
        print("Songs in the playlist : " + str(songTitlesOfAllPlaylists[i]) + "\n")
        print("---------------------------------------------------------------------------------------\n")
        i = i+1


def prepareYouTubeSongUrls(videoIds):
    for videoId in videoIds:
        songYoutubeURLList.append(YOUTUBE_BASE_URL + videoId)


def downloadSongFromYoutube(song_url):
    with youtube_dl.YoutubeDL(download_options) as dl:
        return song_url + " : " + str(dl.download([song_url]))


def downloadSongs():
    with concurrent.futures.ThreadPoolExecutor(NO_OF_THREADS) as executor:
        statusList = executor.map(downloadSongFromYoutube, songYoutubeURLList)

    for status in statusList:
        print('\n' + status)


def displaySongsInAPlaylist(songList):
    i = 1
    print("The playlist you selected has the following songs -- \n")
    for song in songList:
        print(str(i)+". "+song+"\n")
        i = i + 1


DOWNLOAD_FOLDER = 'YouTubeDownloads'
DOWNLOAD_LOCATION = '/tmp'
YOUTUBE_BASE_URL = "https://www.youtube.com/watch?v="
GOOGLE_API_KEY = "AIzaSyApLwmFqEBOS_bxj1DJRv_ULwWO-PKWQLY"
NO_OF_PLAYLIST_TO_DISPLAY = 6
MAXIMUM_NUMBER_OF_SONGS_TO_DOWNLOAD = 400
NO_OF_THREADS = 50

songYoutubeURLList = []
playListIds = []
playListTitles = []
songTitlesOfAllPlaylists = []
videoIdsOfAllPlaylists = []

PLAYLIST_SEARCH = input("\nPlease enter the search string for your playlist : ")
print("\nSongs will be downloaded in a newly created folder 'YouTubeDownloads' under '/tmp' by default.")
change_folder = input("\nDo you want do change the download location to something else (y for yes | anything else for no) : ")
if change_folder == 'y':
    DOWNLOAD_LOCATION = input("\nEnter download location : ")
DIRECTORY = DOWNLOAD_LOCATION + "/" + DOWNLOAD_FOLDER
createDir(DIRECTORY)
getYouTubePlaylists()
getAllSongsFromAllPlayLists()
displayPlaylistWithItsSongs()
user_input = input('\nWhich playlist should we download for you : ')
displaySongsInAPlaylist(songTitlesOfAllPlaylists[int(user_input)-1])
prepareYouTubeSongUrls(videoIdsOfAllPlaylists[int(user_input)-1])
downloadSongs()
