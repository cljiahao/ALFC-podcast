from src.ytPlaylist import ytPlaylist
from src.ytDownload import ytDownload
from src.spotifyUpload import spotifyUpload

# TODO create a chinese version
# See if combine two playlists and upload them accordingly instead of having to create two sets of files. 
# Problem would be if one fails, the github action might fail too. Probably splitting might be better?

channelURL = "https://www.youtube.com/playlist?list=PLZ1GiYqZoiH7QyULF8B7Wm5jeveptXaQG"
srcPath = "spotify"

if __name__ == "__main__":
    playlist = ytPlaylist(channelURL).newVideos
    fileNames = ytDownload(srcPath,playlist).fileNames
    spotifyUpload(fileNames)