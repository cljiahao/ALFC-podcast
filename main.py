from src.ytPlaylist import ytPlaylist
from src.ytDownload import ytDownload
from src.spotifyUpload import spotifyUpload

channelURLs = {
    "Eng": "https://www.youtube.com/playlist?list=PLZ1GiYqZoiH7QyULF8B7Wm5jeveptXaQG",
    "Chi": "https://www.youtube.com/playlist?list=PLZ1GiYqZoiH7V3xNi_DpCC0yXNbWPPvAK",
}

if __name__ == "__main__":
    for lang, url in channelURLs.items():
        srcPath = "spotify"
        playlist = ytPlaylist(lang, url).newVideos
        fileNames = ytDownload(srcPath, lang, playlist).fileNames
        if len(fileNames) > 0:
            spotifyUpload(lang, srcPath, fileNames)
