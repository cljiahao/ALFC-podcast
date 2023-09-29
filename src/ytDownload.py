import os
import re
import json
import time
from yt_dlp import YoutubeDL
from datetime import datetime

class ytDownload():
    def __init__(self,srcPath,lang,playlist):
        srcPath = srcPath+f"/{lang}"
        self.process(srcPath,playlist)
        print("Done downloading")
        self.renameFiles(srcPath,lang)

    def process(self,srcPath,playlist):

        ydl_opts = {
            'format': 'mp3/bestaudio/best',
            'outtmpl': '{}/%(title)s.%(ext)s'.format(srcPath),
            'postprocessors': [{  # Extract audio using ffmpeg
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }]
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download(playlist)

    def jsonRead(self,lang):
        with open(f"src/json/{lang}Podcast.json", "r") as f:
            return json.load(f)

    def jsonWrite(self,lang,data):
        with open(f"src/json/{lang}Podcast.json", "w") as f:
            json.dump(data,f)

    def renameFiles(self,srcPath,lang):
        newPod, arr, self.fileNames = [],[],[]

        oldPod = self.jsonRead(lang)

        for fileName in os.listdir(srcPath):
            if fileName.split(".")[-1] == "mp3":
                match = re.search(r'\d{1,2} \b\w{1,4} \d{4}',fileName)
                for fmt in ('%d %b %Y','%d %B %Y'):
                    try: 
                        newPod.append([datetime.strptime(match.group(), fmt).date(),fileName,False])
                        break
                    except ValueError: pass
        
        
        if not self.jsonRead(lang)[0][0]:
            sortDict = sorted(newPod) 
        else:
            oldPod = [[datetime.strptime(x[0], '%d %b %Y').date(),x[1],x[2]] for x in oldPod]
            for i,j in enumerate(newPod):
                if j[0] in [x[0]for x in oldPod]: newPod.pop(i)
            sortDict = sorted(newPod+oldPod)

        for i, data in enumerate(sortDict):
            newName = f"{i+1}. ALFC Devotional - {datetime.strftime(data[0],'%d %b %Y')}.mp3"
            if not data[2]:
                self.fileNames.append(newName)
                os.rename(os.path.join(srcPath,data[1]),os.path.join(srcPath,newName))
            arr.append([datetime.strftime(data[0],'%d %b %Y'),newName,True])
        
        self.jsonWrite(lang,arr)

            