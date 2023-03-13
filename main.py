from src.ytPlaylist import ytPlaylist
from src.ytDownload import ytDownload
from src.spotifyUpload import spotifyUpload

channelURLs = {
    "Eng":"https://www.youtube.com/playlist?list=PLZ1GiYqZoiH7QyULF8B7Wm5jeveptXaQG",
    "Chi":"https://www.youtube.com/playlist?list=PLZ1GiYqZoiH7V3xNi_DpCC0yXNbWPPvAK"
    }
srcPath = "spotify"

if __name__ == "__main__":
    for lang,url in channelURLs.items():
        playlist = ytPlaylist(lang,url).newVideos
        fileNames = ytDownload(srcPath,lang,playlist).fileNames
        spotifyUpload(lang,fileNames)