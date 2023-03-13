import json
from pytube import Playlist

class ytPlaylist():
    def __init__(self,lang,channel):
        oldList = self.jsonRead(lang)
        self.extractList(lang,channel,oldList)

    def jsonRead(self,lang):
        with open(f"src/json/{lang}playlist.json", "r") as f:
            return json.load(f)

    def jsonWrite(self,lang,data):
        with open(f"src/json/{lang}playlist.json", "w") as f:
            json.dump(data,f)
    
    def extractList(self,lang,channel,oldList):
        playlist = Playlist(channel)
        self.jsonWrite(lang,list(playlist))
        self.newVideos = [x for x in playlist if x not in set(oldList)]
